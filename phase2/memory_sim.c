#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

#define MEMORY_SIZE 1024  // 1 KB block
#define BLOCK_SIZE 32     // 32 bytes per block
#define TOTAL_BLOCKS (MEMORY_SIZE / BLOCK_SIZE)

bool memory_map[TOTAL_BLOCKS];   // 0 = free, 1 = used
char memory[MEMORY_SIZE];        // simulated memory

void init_memory() {
    memset(memory_map, 0, sizeof(memory_map));
    printf("Memory Initialized: %d blocks of %d bytes\n", TOTAL_BLOCKS, BLOCK_SIZE);
}

void* my_malloc(int size) {
    int blocks_needed = (size + BLOCK_SIZE - 1) / BLOCK_SIZE;
    int free_count = 0;

    for (int i = 0; i < TOTAL_BLOCKS; i++) {
        if (memory_map[i] == 0) {
            free_count++;
            if (free_count == blocks_needed) {
                int start = i - blocks_needed + 1;
                for (int j = start; j <= i; j++)
                    memory_map[j] = 1;

                return &memory[start * BLOCK_SIZE];
            }
        } else {
            free_count = 0;
        }
    }

    return NULL; // No memory
}

void my_free(void* ptr) {
    int index = ((char*)ptr - memory) / BLOCK_SIZE;
    if (index >= 0 && index < TOTAL_BLOCKS) {
        memory_map[index] = 0;
        printf("Freed block %d\n", index);
    }
}

void show_memory_map() {
    printf("Memory Map: ");
    for (int i = 0; i < TOTAL_BLOCKS; i++)
        printf("%d", memory_map[i]);
    printf("\n");
}

int main() {
    init_memory();

    void* p1 = my_malloc(64);
    show_memory_map();

    void* p2 = my_malloc(128);
    show_memory_map();

    my_free(p1);
    show_memory_map();

    return 0;
}

