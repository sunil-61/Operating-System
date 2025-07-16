import tkinter as tk
from tkinter import filedialog, messagebox

def run(parent_frame):
    parent_frame.config(bg='white')

    text_area = tk.Text(parent_frame, wrap='word', font=("Arial", 12))
    text_area.pack(expand=True, fill='both', padx=10, pady=10)

    def save_file():
        file = filedialog.asksaveasfilename(defaultextension=".txt")
        if file:
            with open(file, 'w') as f:
                f.write(text_area.get("1.0", 'end-1c'))
            messagebox.showinfo("Saved", "File saved successfully!")

    def open_file():
        file = filedialog.askopenfilename()
        if file:
            with open(file, 'r') as f:
                text_area.delete("1.0", 'end')
                text_area.insert("1.0", f.read())

    toolbar = tk.Frame(parent_frame, bg='lightgray')
    toolbar.pack(fill='x')

    tk.Button(toolbar, text="🗂️ Open", command=open_file).pack(side='left', padx=5, pady=5)
    tk.Button(toolbar, text="💾 Save", command=save_file).pack(side='left', padx=5, pady=5)

