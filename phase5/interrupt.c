#include <stdio.h>

void handle_interrupt(long arg) {
    printf("⚡ Interrupt received! Value = %ld\n", arg);
}

