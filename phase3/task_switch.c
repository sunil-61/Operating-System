#include <stdio.h>
#include <setjmp.h>
#include <unistd.h>

jmp_buf env1, env2;
int current = 1;

void task1() {
    for (int i = 0; i < 5; i++) {
        printf("🟢 Task 1 running: iteration %d\n", i+1);
        sleep(1);
        if (!setjmp(env1)) longjmp(env2, 1);  // Switch to Task 2
    }
}

void task2() {
    for (int i = 0; i < 5; i++) {
        printf("🔵 Task 2 running: iteration %d\n", i+1);
        sleep(1);
        if (!setjmp(env2)) longjmp(env1, 1);  // Switch to Task 1
    }
}

int main() {
    printf("🔁 Starting Task Switching Simulation...\n");

    if (!setjmp(env1)) task2();  // Start with Task 2 (so task1 will resume first)
    task1();

    printf("✅ Task Switching Completed\n");
    return 0;
}

