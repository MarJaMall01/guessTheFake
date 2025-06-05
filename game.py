import tkinter as tk
import random
from news_api import fetch_news
from rag_handler import rag_model, get_a_news

# global variables for score and fake random choice
score = 0
is_fake = False

def run_round(game_window, main_frame, collection, default_prompt):
    global is_fake

    is_fake = random.choice([True, False])
    print(f"DEBUG: is_fake = {is_fake}")

    if is_fake:
        # Fake News generieren lassen
        news_text = get_a_news(collection=collection, default_prompt=default_prompt)
    else:
        # Original aus DB holen
        all_docs = collection.get()["documents"]
        if not all_docs:
            news_text = "Keine Nachricht verfügbar."
        else:
            news_text = random.choice(all_docs)

    # Frame leeren
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Text anzeigen (mehrzeilig)
    text_label = tk.Label(
        main_frame,
        text=news_text,
        font=("Helvetica", 18),
        bg="#f0f4f7",
        fg="#333",
        wraplength=1000,
        justify="left"
    )
    text_label.pack(pady=30)

    # Punktestand
    tk.Label(
        main_frame,
        text=f"Punkte: {score}",
        font=("Helvetica", 18),
        bg="#f0f4f7",
        fg="#555"
    ).pack(pady=10)

    # Bewertungsbuttons
    def evaluate_choice(user_says_fake):
        global score
        if user_says_fake == is_fake:
            score += 1
            print("Richtige Entscheidung!")
        else:
            print("Falsche Entscheidung!")
            score = 0
        run_round(game_window, main_frame, collection, default_prompt)

    # Buttons
    tk.Button(
        main_frame, text="Fake", bg="#f44336", fg="white",
        font=("Helvetica", 14, "bold"),
        command=lambda: evaluate_choice(True)
    ).pack(pady=10)

    tk.Button(
        main_frame, text="Echt", bg="#4CAF50", fg="white",
        font=("Helvetica", 14, "bold"),
        command=lambda: evaluate_choice(False)
    ).pack(pady=10)


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

        run_round(game_window, main_frame, collection, default_prompt)

        game_window.mainloop()
    else:
        print("Fehler beim Abrufen der Nachrichten.")
