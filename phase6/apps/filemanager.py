import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog

# Internal simulated storage folder
STORAGE_DIR = os.path.expanduser("~/mini_os_storage")
os.makedirs(STORAGE_DIR, exist_ok=True)

# Main entry point for embedding into OS GUI
def run(parent_frame):
    for widget in parent_frame.winfo_children()[1:]:
        widget.destroy()


    parent_frame.configure(bg='white')

    path_stack = [STORAGE_DIR]  # To track navigation history

    # Path label
    path_label = tk.Label(parent_frame, text=STORAGE_DIR, anchor='w', bg='lightgray')
    path_label.pack(fill='x')

    # Treeview area
    tree = ttk.Treeview(parent_frame)
    tree.pack(fill='both', expand=True, padx=5, pady=5)

    def populate_tree(path, parent=""):
        try:
            items = os.listdir(path)
            for item in sorted(items):
                abs_path = os.path.join(path, item)
                node = tree.insert(parent, 'end', text=item, open=False)
                if os.path.isdir(abs_path):
                    tree.insert(node, 'end')  # dummy child
        except Exception as e:
            print(f"Error: {e}")

    def update_tree(event):
        node = tree.focus()
        path = get_full_path(node)
        if os.path.isdir(path):
            tree.delete(*tree.get_children(node))
            populate_tree(path, node)

    def get_full_path(node):
        path_parts = []
        while node:
            path_parts.insert(0, tree.item(node)['text'])
            node = tree.parent(node)
        return os.path.join(*path_stack, *path_parts[1:])

    def open_selected():
        node = tree.focus()
        path = get_full_path(node)
        if os.path.isfile(path):
            with open(path, 'r') as f:
                content = f.read()
            edit_window = tk.Toplevel(parent_frame)
            edit_window.title(os.path.basename(path))
            txt = tk.Text(edit_window, wrap='word')
            txt.insert('1.0', content)
            txt.pack(fill='both', expand=True)

            def save():
                with open(path, 'w') as f:
                    f.write(txt.get('1.0', 'end-1c'))
                messagebox.showinfo("Saved", f"Saved {path}")
                edit_window.destroy()

            tk.Button(edit_window, text="Save", command=save).pack(pady=5)
        else:
            messagebox.showinfo("Info", "Not a file")

    def delete_selected():
        node = tree.focus()
        path = get_full_path(node)
        if messagebox.askyesno("Confirm", f"Delete {path}?"):
            try:
                if os.path.isfile(path):
                    os.remove(path)
                else:
                    os.rmdir(path)
                tree.delete(node)
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def create_file():
        filename = simpledialog.askstring("New File", "Enter filename:")
        if filename:
            full_path = os.path.join(path_stack[-1], filename)
            try:
                open(full_path, 'w').close()
                refresh_tree()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def create_folder():
        foldername = simpledialog.askstring("New Folder", "Enter folder name:")
        if foldername:
            full_path = os.path.join(path_stack[-1], foldername)
            try:
                os.makedirs(full_path)
                refresh_tree()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def go_back():
        if len(path_stack) > 1:
            path_stack.pop()
            refresh_tree()

    def refresh_tree():
        path_label.config(text=path_stack[-1])
        for item in tree.get_children():
            tree.delete(item)
        populate_tree(path_stack[-1])

    # Buttons
    btn_frame = tk.Frame(parent_frame, bg='white')
    btn_frame.pack(fill='x', pady=5)

    tk.Button(btn_frame, text="📁 New Folder", command=create_folder).pack(side='left', padx=4)
    tk.Button(btn_frame, text="📄 New File", command=create_file).pack(side='left', padx=4)
    tk.Button(btn_frame, text="✏️ Edit/Open", command=open_selected).pack(side='left', padx=4)
    tk.Button(btn_frame, text="❌ Delete", command=delete_selected).pack(side='left', padx=4)
    tk.Button(btn_frame, text="🔙 Back", command=go_back).pack(side='left', padx=4)

    tree.bind('<<TreeviewOpen>>', update_tree)

    # Initial load
    refresh_tree()

