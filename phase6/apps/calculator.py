import tkinter as tk

def run(parent_frame):
    parent_frame.config(bg='white')
    expression = tk.StringVar()

    def press(num):
        expression.set(expression.get() + str(num))

    def equal():
        try:
            expression.set(str(eval(expression.get())))
        except:
            expression.set("Error")

    def clear():
        expression.set("")

    entry = tk.Entry(parent_frame, textvariable=expression, font=("Arial", 18))
    entry.pack(pady=10, fill='x', padx=10)

    buttons = [
        '7', '8', '9', '/',
        '4', '5', '6', '*',
        '1', '2', '3', '-',
        'C', '0', '=', '+'
    ]

    btn_frame = tk.Frame(parent_frame)
    btn_frame.pack()

    for i, b in enumerate(buttons):
        cmd = equal if b == '=' else (clear if b == 'C' else lambda x=b: press(x))
        tk.Button(btn_frame, text=b, width=5, height=2, command=cmd).grid(row=i//4, column=i%4, padx=2, pady=2)

