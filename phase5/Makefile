all:
	nasm -f elf64 interrupt.asm -o interrupt.o
	gcc -nostartfiles interrupt.o interrupt.c -o interrupt_sim

	nasm -f elf64 trap_sim.asm -o trap_sim.o
	gcc -nostartfiles trap_sim.o trap_sim.c -o trap_sim -lc -e _start

run:
	./interrupt_sim
	./trap_sim

