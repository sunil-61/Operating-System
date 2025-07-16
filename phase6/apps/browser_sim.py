import tkinter as tk
from tkinter import Entry, Button, messagebox
import webbrowser

# Embedded browser launcher

def run(parent_frame):
    for widget in parent_frame.winfo_children()[1:]:
        widget.destroy()


    parent_frame.configure(bg='white')

    heading = tk.Label(parent_frame, text="🌐 Mini OS Browser", font=("Arial", 14, "bold"), bg='white')
    heading.pack(pady=10)

    url_entry = Entry(parent_frame, font=("Arial", 12), width=50)
    url_entry.pack(pady=10)

    def open_url():
        url = url_entry.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Please enter a URL")
            return
        if not url.startswith("http"):
            url = "https://" + url
        try:
            webbrowser.open(url)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    open_btn = Button(parent_frame, text="🚀 Launch", font=("Arial", 11), command=open_url)
    open_btn.pack(pady=10)

    url_entry.insert(0, "https://google.com")

    # Auto open Google at start
    open_url()

