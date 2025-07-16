import tkinter as tk
from PIL import Image, ImageTk
import os
import subprocess
from apps import browser_sim, calculator, notes_app, filemanager, command_prompt

# Path configuration
APP_PATH = os.path.join(os.path.dirname(__file__), 'apps')
ICON_PATH = os.path.join(os.path.dirname(__file__), 'icons')

# Taskbar tracking
open_apps = {}

class MiniOS:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini OS - Sonu Edition")
        self.root.geometry("900x600")
        self.root.configure(bg='#202020')

        self.desktop_frame = tk.Frame(self.root, bg='#202020')
        self.desktop_frame.place(x=0, y=0, relwidth=1, relheight=0.95)

        self.create_taskbar()
        self.create_desktop()

    def create_desktop(self):
        self.add_icon("browser", "Browser", lambda: self.launch_app("Browser", browser_sim.run), 50, 100)
        self.add_icon("filemanager", "Filemanager", lambda: self.launch_app("Filemanager", filemanager.run), 150, 100)
        self.add_icon("calculator", "Calculator", lambda: self.launch_app("Calculator", calculator.run), 250, 100)
        self.add_icon("notes", "Notes", lambda: self.launch_app("Notes", notes_app.run), 350, 100)
        self.add_icon("cmd", "Terminal", lambda: self.launch_app("Terminal", command_prompt.run), 450, 100)

        self.add_icon("memory", "Memory Sim", lambda: self.launch_exec_in_frame("Memory Sim", "../phase2/memory_sim"), 50, 200)
        self.add_icon("task", "Task Switch", lambda: self.launch_exec_in_frame("Task Switch", "../phase3/task_switch"), 150, 200)
        self.add_icon("syscall", "Syscall Sim", lambda: self.launch_exec_in_frame("Syscall Sim", "../phase4/syscall_sim"), 250, 200)
        self.add_icon("interrupt", "Interrupt Sim", lambda: self.launch_exec_in_frame("Interrupt Sim", "../phase5/interrupt_sim"), 350, 200)
        self.add_icon("trap", "Trap Sim", lambda: self.launch_exec_in_frame("Trap Sim", "../phase5/trap_sim"), 50, 300)

        

    def add_icon(self, icon_file, name, command, x, y):
        icon_path = os.path.join(ICON_PATH, f"{icon_file}.png")
        if os.path.exists(icon_path):
            img = Image.open(icon_path).resize((64, 64))
            photo = ImageTk.PhotoImage(img)
            icon_btn = tk.Label(self.desktop_frame, image=photo, cursor="hand2", bg='#202020')
            icon_btn.image = photo
            icon_btn.place(x=x, y=y)
            icon_btn.bind("<Button-1>", lambda e: command())
            tk.Label(self.desktop_frame, text=name, fg="white", bg="#202020", font=("Arial", 10)).place(x=x+5, y=y+70)

    def create_taskbar(self):
        self.taskbar = tk.Frame(self.root, bg='black', height=30)
        self.taskbar.pack(side='bottom', fill='x')
        tk.Label(self.taskbar, text="🕒 12:45 PM    🔋 Battery 87%", bg="black", fg="white", font=("Arial", 10)).pack(side="right")

    def add_to_taskbar(self, app_name, frame):
        def toggle():
            if frame.winfo_ismapped():
                frame.place_forget()
                # 🧠 Check: Are all apps minimized?
                all_hidden = all(not f.winfo_ismapped() for f, _ in open_apps.values())
                if all_hidden:
                    self.desktop_frame.place(x=0, y=0, relwidth=1, relheight=0.95)
            else:
                self.desktop_frame.place_forget()  # Hide desktop again
                self.show_frame(frame)

        btn = tk.Button(self.taskbar, text=app_name, command=toggle, height=1)
        btn.pack(side='left', padx=2)
        open_apps[app_name] = (frame, btn)


    def show_frame(self, frame):
        for child in self.root.winfo_children():
            if isinstance(child, tk.Frame) and child != self.taskbar:
                child.place_forget()
        frame.place(x=0, y=0, relwidth=1, relheight=0.95)

    def launch_app(self, app_name, command):
        if app_name in open_apps:
            self.show_frame(open_apps[app_name][0])
            return

        self.desktop_frame.place_forget()  # Hide desktop

        app_frame = tk.Frame(self.root, bg='white')

        # Add Close Button
        close_btn = tk.Button(app_frame, text="❌ Close", bg="red", fg="white",
                              command=lambda: self.close_current_app(app_name))
        close_btn.pack(anchor="ne", padx=5, pady=5)

        command(app_frame)  # Run app GUI
        self.show_frame(app_frame)
        self.add_to_taskbar(app_name, app_frame)

    def close_current_app(self, app_name):
        if app_name in open_apps:
            open_apps[app_name][0].place_forget()
            open_apps[app_name][1].destroy()
            del open_apps[app_name]
            self.desktop_frame.place(x=0, y=0, relwidth=1, relheight=0.95)

    def launch_exec(self, path):
        try:
            subprocess.Popen([path])
        except FileNotFoundError:
            print(f"[ERROR] Executable not found: {path}")

    def launch_exec_in_frame(self, app_name, path):
        from subprocess import Popen, PIPE
        app_frame = tk.Frame(self.root, bg='black')

        close_btn = tk.Button(app_frame, text="❌ Close", bg="red", fg="white", command=lambda: self.close_current_app(app_name))
        close_btn.pack(anchor="ne", padx=5, pady=5)

        output_text = tk.Text(app_frame, bg='black', fg='white', font=("Courier", 10))
        output_text.pack(fill='both', expand=True, padx=5, pady=5)

        try:
            process = Popen([path], stdout=PIPE, stderr=PIPE, text=True)
            stdout, stderr = process.communicate()
            output_text.insert('end', stdout)
            if stderr:
                output_text.insert('end', "\n[ERROR]\n" + stderr)
        except FileNotFoundError:
            output_text.insert('end', f"[ERROR] Executable not found: {path}")

        self.show_frame(app_frame)
        self.add_to_taskbar(app_name, app_frame)

if __name__ == '__main__':
    root = tk.Tk()
    os_system = MiniOS(root)
    root.mainloop()

