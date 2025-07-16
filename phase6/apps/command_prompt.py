import tkinter as tk
from tkinter import messagebox
import subprocess
import os

PHASE_EXEC_PATHS = {
    "memory": "../phase2/memory_sim",
    "task": "../phase3/task_switch",
    "syscall": "../phase4/syscall_sim",
    "interrupt": "../phase5/interrupt_sim",
    "trap": "../phase5/trap_sim"
}

def run(parent_frame):
    for widget in parent_frame.winfo_children():
        widget.destroy()

    parent_frame.configure(bg='black')

    terminal_label = tk.Label(parent_frame, text="MiniOS Terminal", fg='white', bg='black', font=("Consolas", 12, "bold"))
    terminal_label.pack(pady=5)

    output_box = tk.Text(parent_frame, bg='black', fg='lime', font=("Consolas", 10), wrap='word')
    output_box.pack(expand=True, fill='both', padx=10, pady=5)

    command_entry = tk.Entry(parent_frame, font=("Consolas", 10), bg='gray20', fg='white')
    command_entry.pack(fill='x', padx=10, pady=5)

    def execute_command():
        cmd = command_entry.get().strip().lower()
        command_entry.delete(0, 'end')
        if cmd.startswith("run "):
            phase = cmd.split(" ")[1]
            exe_path = PHASE_EXEC_PATHS.get(phase)
            if exe_path:
                output_box.insert('end', f"> {cmd}\n")
                try:
                    process = subprocess.Popen([exe_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    stdout, stderr = process.communicate()
                    output_box.insert('end', stdout)
                    if stderr:
                        output_box.insert('end', f"\n[ERROR]\n{stderr}")
                except Exception as e:
                    output_box.insert('end', f"\n[EXCEPTION] {e}\n")
            else:
                output_box.insert('end', f"[ERROR] Phase '{phase}' not found.\n")
        else:
            output_box.insert('end', "[!] Unknown command.\n")
        output_box.insert('end', '\n')
        output_box.see('end')

    run_button = tk.Button(parent_frame, text="Execute", command=execute_command, bg='gray30', fg='white')
    run_button.pack(pady=5)

    command_entry.bind("<Return>", lambda e: execute_command())

