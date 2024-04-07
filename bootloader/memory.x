/*
 * Automatically generated by PATINA; edits will be discarded on rebuild.
 * (Most header files phrase this 'Do not edit.'; be warned accordingly.)
 *
 * Generated: 2024-04-07 16:55:32.564846.
 */

MEMORY {
    BASICMEMORY : ORIGIN = 0x00000000, LENGTH = 0x2000
    BOOTMEM : ORIGIN = 0x00002000, LENGTH = 0x200
}


    
EXTERN(__start);
ENTRY(__start);

SECTIONS {
    PROVIDE(__stack_start = ORIGIN(BASICMEMORY) + LENGTH(BASICMEMORY));
    PROVIDE(__stext = ORIGIN(BOOTMEM));

    .text __stext : {
        *(.start);

        *(.text .text.*);

        . = ALIGN(4);
        __etext = .;
    } > BOOTMEM

    .rodata : ALIGN(4) {
        . = ALIGN(4);
        __srodata = .;
        *(.rodata .rodata.*);
        . = ALIGN(4);
        __erodata = .;
    } > BOOTMEM

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
    

