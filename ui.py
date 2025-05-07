import tkinter as tk

def create_buttons(parent_frame):
    buttons_frame = tk.Frame(parent_frame, bg="#f0f4f7")
    buttons_frame.pack(side="bottom", pady=50)

    button_style = {
        "font": ("Helvetica", 24, "bold"),
        "width": 12,
        "height": 2,
        "bg": "#4CAF50",
        "fg": "white",
        "activebackground": "#45a049",
        "activeforeground": "white",
        "bd": 0,
        "relief": "flat",
        "cursor": "hand2"
    }

    real_button = tk.Button(buttons_frame, text="Echt", **button_style)
    real_button.grid(row=0, column=0, padx=50, pady=20)

    fake_button_style = button_style.copy()
    fake_button_style["bg"] = "#f44336"
    fake_button_style["activebackground"] = "#e53935"

    fake_button = tk.Button(buttons_frame, text="Fake", **fake_button_style)
    fake_button.grid(row=0, column=1, padx=50, pady=20)
