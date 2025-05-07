import tkinter as tk
from news_api import fetch_news
from rag_handler import rag_model, get_a_news

def start_game(root):
    print("Game started!")
    news_data = fetch_news()
    if news_data:
        collection = rag_model(news_data)
        with open("default_prompt.txt", "r", encoding="utf-8") as file:
            default_prompt = file.read()

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.destroy()

        game_window = tk.Tk()
        game_window.title("Game Window")
        game_window.geometry(f"{screen_width}x{screen_height}")
        game_window.configure(bg="#f0f4f7")

        main_frame = tk.Frame(game_window, bg="#f0f4f7")
        main_frame.pack(fill="both", expand=True)

        title_label = tk.Label(
            main_frame,
            text=get_a_news(collection=collection, default_prompt=default_prompt),
            font=("Helvetica", 32, "bold"),
            bg="#f0f4f7",
            fg="#333",
            wraplength=800,
            justify="center"
        )
        title_label.pack(pady=40)

        content_text = tk.Label(
            main_frame,
            text="Hier steht der News-Inhalt...",
            font=("Helvetica", 20),
            bg="#f0f4f7",
            fg="#555",
            wraplength=1000,
            justify="center"
        )
        content_text.pack(pady=20)

        from ui import create_buttons
        create_buttons(main_frame)

        game_window.mainloop()
    else:
        print("Fehler beim Abrufen der Nachrichten.")
