/*
 * Automatically generated by PATINA; edits will be discarded on rebuild.
 * (Most header files phrase this 'Do not edit.'; be warned accordingly.)
 *
 * Generated: 2024-03-23 22:26:05.160328.
 */

MEMORY {
    spram : ORIGIN = 0x00000000, LENGTH = 0x8000
    spram2 : ORIGIN = 0x00008000, LENGTH = 0x8000
    mem : ORIGIN = 0x00010000, LENGTH = 0x2000
    boot : ORIGIN = 0x00014000, LENGTH = 0x200
}


SECTIONS {
    PROVIDE(__stack_start = ORIGIN(mem) + LENGTH(mem));
    PROVIDE(__stext = ORIGIN(boot);
    
    .text __stext : {
        *(.start);

        *(.text .text.*);

        . = ALIGN(4);
        __etext = .;
    } > boot

    .rodata : ALIGN(4) {
        . = ALIGN(4);
        __srodata = .;
        *(.rodata .rodata.*);
        . = ALIGN(4);
        __erodata = .;
    } > boot

    /DISCARD/ : {
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
    }
}
    

