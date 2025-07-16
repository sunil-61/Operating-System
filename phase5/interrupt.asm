section .text
global _start

extern handle_interrupt

_start:
    mov rdi, 42              ; argument pass
    call handle_interrupt    ; call C function
    mov rax, 60              ; syscall exit
    xor rdi, rdi
    syscall

