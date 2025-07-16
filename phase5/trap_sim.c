#include <stdio.h>

void handle_trap(int syscall_no) {
    switch(syscall_no) {
        case 1:
            printf("[TRAP] System Call: PRINT -> Hello from TRAP!\n");
            break;
        case 2:
            printf("[TRAP] System Call: ADD -> 4 + 5 = %d\n", 4 + 5);
            break;
        case 3:
            printf("[TRAP] System Call: EXIT -> Exiting via trap...\n");
            break;
        default:
            printf("[TRAP] Unknown system call!\n");
    }
}

void trap_entry() {
    printf("[TRAP] Trap received. Dispatching to handler...\n");
    handle_trap(1);
    handle_trap(2);
    handle_trap(3);
}

