#
# This file was part of LUNA.
#
# Copyright (c) 2023 Great Scott Gadgets <info@greatscottgadgets.com>
# SPDX-License-Identifier: BSD-3-Clause
# lifted from https://github.com/greatscottgadgets/luna-soc ( 319901c )

"""Generate Rust support files for SoC designs."""

import datetime
import logging
from hapenny.mem import BasicMemory,SpramMemory

class GenRust:
    def __init__(self, soc):
        self._soc = soc

    # - memory.x generation ---------------------------------------------------
    def generate_memory_x(self, file=None):
        """ Generate a memory.x file for the given SoC"""

        def emit(content):
            """ Utility function that emits a string to the targeted file. """
            print(content, file=file)

        # warning header
        emit("/*")
        emit(" * Automatically generated by PATINA; edits will be discarded on rebuild.")
        emit(" * (Most header files phrase this 'Do not edit.'; be warned accordingly.)")
        emit(" *")
        emit(f" * Generated: {datetime.datetime.now()}.")
        emit(" */")
        emit("")

        # memory regions
        regions = set()
        emit("MEMORY {")
        for i in self._soc.memory_map.all_resources():
            res = i.resource
            name = i.resource.name.upper()
            start = i.start
            sec_length = i.end - i.start
            if not isinstance(res,(BasicMemory,SpramMemory)):
                continue
            emit(f"    {name} : ORIGIN = 0x{start:08x}, LENGTH = 0x{sec_length:0x}")
            regions.add(name)
        emit("}")
        emit("")   
        self.extra(regions,emit)
        emit("")

    def extra(self,regions,emit):
        ram = "mem" if "mem" in regions else "mem"
        aliases = {
            "REGION_TEXT":   ram,
            "REGION_RODATA": ram,
            "REGION_DATA":   ram,
            "REGION_BSS":    ram,
            "REGION_HEAP":   ram,
            "REGION_STACK":  ram,
        }
        for alias, region in aliases.items():
            emit(f"REGION_ALIAS(\"{alias}\", {region});")
        
class BootLoaderX(GenRust):
    def __init__(self,soc):
        super().__init__(soc)
    
    def extra(self,regions,emit):
        chunk = """
    
    EXTERN(__start);
    ENTRY(__start);

SECTIONS {{
    PROVIDE(__stack_start = ORIGIN({mem}) + LENGTH({mem}));
    PROVIDE(__stext = ORIGIN({boot}));

    .text __stext : {{
        *(.start);

        *(.text .text.*);

        . = ALIGN(4);
        __etext = .;
    }} > {boot}

    .rodata : ALIGN(4) {{
        . = ALIGN(4);
        __srodata = .;
        *(.rodata .rodata.*);
        . = ALIGN(4);
        __erodata = .;
    }} > {boot}

    /DISCARD/ : {{
        /* throw away RAM sections to get a link error if they're used. */
        *(.bss);
        *(.bss.*);
        *(.data);
        *(.data.*);
        *(COMMON);
        *(.ARM.exidx);
        *(.ARM.exidx.*);
        *(.ARM.extab.*);
        *(.got);
    }}
}}
    """
        emit(chunk.format(mem="MEM",boot="BOOT"))
