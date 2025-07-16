#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

#define MEMORY_SIZE 1024
#define BLOCK_SIZE 32
#define TOTAL_BLOCKS (MEMORY_SIZE / BLOCK_SIZE)

typedef struct {
    bool used;
    int block_count; // only valid in first block of allocated segment
} BlockMetadata;

BlockMetadata metadata[TOTAL_BLOCKS];
char memory[MEMORY_SIZE];

void init_memory() {
    for (int i = 0; i < TOTAL_BLOCKS; i++) {
        metadata[i].used = false;
        metadata[i].block_count = 0;
    }
    printf("Memory Initialized: %d blocks of %d bytes\n", TOTAL_BLOCKS, BLOCK_SIZE);
}

void* my_malloc(int size) {
    int blocks_needed = (size + BLOCK_SIZE - 1) / BLOCK_SIZE;
    int free_count = 0;

    for (int i = 0; i < TOTAL_BLOCKS; i++) {
        if (!metadata[i].used) {
            free_count++;
            if (free_count == blocks_needed) {
                int start = i - blocks_needed + 1;
                metadata[start].block_count = blocks_needed;

                for (int j = start; j <= i; j++)
                    metadata[j].used = true;

                printf("Allocated %d blocks starting at block %d\n", blocks_needed, start);
                return &memory[start * BLOCK_SIZE];
            }
        } else {
            free_count = 0;
        }
    }

    printf("Allocation failed: Not enough memory.\n");
    return NULL;
}

void my_free(void* ptr) {
    int index = ((char*)ptr - memory) / BLOCK_SIZE;

    if (index < 0 || index >= TOTAL_BLOCKS || !metadata[index].used) {
        printf("Invalid free operation!\n");
        return;
    }

    int blocks = metadata[index].block_count;

    for (int i = index; i < index + blocks; i++) {
        metadata[i].used = false;
        metadata[i].block_count = 0;
    }

    printf("Freed %d blocks starting at block %d\n", blocks, index);
}

void show_memory_map() {
    printf("Memory Map: ");
    for (int i = 0; i < TOTAL_BLOCKS; i++)
        printf("%c", metadata[i].used ? '#' : '.');
    printf("\n");
}

int main() {
    init_memory();

    void* p1 = my_malloc(96);   // 3 blocks
    show_memory_map();

    void* p2 = my_malloc(128);  // 4 blocks
    show_memory_map();

    my_free(p1);
    show_memory_map();

    void* p3 = my_malloc(160);  // 5 blocks
    show_memory_map();

    return 0;
}

