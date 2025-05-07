import tkinter as tk
from game import start_game

root = tk.Tk()
root.title("Get the fake")
root.geometry("300x250")
root.configure(bg="#f0f4f7")

title_label = tk.Label(
    root,
    text="Get the fake",
    font=("Helvetica", 20, "bold"),
    bg="#f0f4f7",
    fg="#333"
)
title_label.pack(pady=30)

start_button = tk.Button(
    root,
    text="Start",
    command=lambda: start_game(root),
    font=("Helvetica", 14, "bold"),
    bg="#2196F3",
    fg="white",
    activebackground="#1976D2",
    activeforeground="white",
    width=12,
    height=2,
    bd=0,
    relief="flat",
    cursor="hand2"
)
start_button.pack(pady=10)

root.mainloop()
