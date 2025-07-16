section .text
    global _start
    extern trap_entry

_start:
    call trap_entry
    mov rax, 60       ; syscall for exit
    xor rdi, rdi      ; status 0
    syscall

