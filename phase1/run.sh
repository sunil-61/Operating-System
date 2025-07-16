#!/bin/bash

nasm -f bin bootloader.asm -o os_image.bin
qemu-system-x86_64 -drive format=raw,file=os_image.bin

