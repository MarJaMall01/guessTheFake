import tkinter as tk

def start_game():
    print("Game started!")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    root.destroy()

    game_window = tk.Tk()
    game_window.title("Game Window")
    game_window.geometry(f"{screen_width}x{screen_height}")

    # -------------- Hauptstruktur -----------------
    # main frame for the game window
    main_frame = tk.Frame(game_window)
    main_frame.pack(fill="both", expand=True)

    # news title
    title_label = tk.Label(
        main_frame, 
        text="News Titel kommt hier hin",
        font=("Helvetica", 28, "bold"),
        wraplength=800,
        justify="center"
    )
    title_label.pack(pady=40)

    # news content
    content_text = tk.Label(
        main_frame, 
        text="Hier steht der News-Inhalt...",
        font=("Helvetica", 18),
        wraplength=1000,
        justify="center"
    )
    content_text.pack(pady=20)

    # buttons for real and fake
    buttons_frame = tk.Frame(main_frame)
    buttons_frame.pack(side="bottom", pady=50)

    real_button = tk.Button(
        buttons_frame, 
        text="Echt", 
        font=("Helvetica", 24),
        width=10,
        height=3
    )
    real_button.grid(row=0, column=0, padx=50, pady=20)

    fake_button = tk.Button(
        buttons_frame, 
        text="Fake", 
        font=("Helvetica", 24),
        width=10,
        height=3
    )
    fake_button.grid(row=0, column=1, padx=50, pady=20)

    game_window.mainloop()

root = tk.Tk()
root.title("Get the fake")
root.geometry("300x200")

title_label = tk.Label(root, text="Get the fake", font=("Helvetica", 16))
title_label.pack(pady=20)

start_button = tk.Button(root, text="Start", command=start_game, font=("Helvetica",12))
start_button.pack(pady=10)

root.mainloop()