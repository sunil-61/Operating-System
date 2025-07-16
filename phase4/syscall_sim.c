#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Simulated system call numbers
#define SYSCALL_PRINT 1
#define SYSCALL_ADD   2
#define SYSCALL_EXIT  3

// Simulated system call handler
int syscall_handler(int syscall_no, void* arg1, void* arg2) {
    switch(syscall_no) {
        case SYSCALL_PRINT:
            printf("🔔 [SYS_PRINT]: %s\n", (char*)arg1);
            return 0;

        case SYSCALL_ADD:
            return (*(int*)arg1 + *(int*)arg2);

        case SYSCALL_EXIT:
            printf("🚪 [SYS_EXIT]: Program exiting\n");
            exit(0);

        default:
            printf("❌ Unknown system call: %d\n", syscall_no);
            return -1;
    }
}

// Simulated user space syscall interface
int syscall(int syscall_no, void* arg1, void* arg2) {
    // In real OS, this would trap into kernel
    return syscall_handler(syscall_no, arg1, arg2);
}

int main() {
    char msg[] = "Hello from Task!";
    syscall(SYSCALL_PRINT, msg, NULL);

    int a = 5, b = 7;
    int sum = syscall(SYSCALL_ADD, &a, &b);
    printf("🔢 [Result of SYS_ADD]: %d + %d = %d\n", a, b, sum);

    syscall(SYSCALL_EXIT, NULL, NULL);

    return 0;
}

