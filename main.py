import tkinter as tk
import ollama as lama
import chromadb as db
import requests
import random

#random number generator for the news
def random_number(x):
    return random.randint(0, x)

#fetch news from the tagesschau api

def fetch_news():
    ressorts = ["inland", "ausland", "wirtschaft", "sport", "kultur", "wissen", "politik"]
    baseUrl = "https://www.tagesschau.de/api2u/news/"
    url = f"{baseUrl}?regions={random_number(15)+1}&ressort={ressorts[random_number(len(ressorts) - 1)]}" 
    try:
        response = requests.get(url)
        response.raise_for_status() # Überprüft, ob der HTTP-Statuscode ein Fehler ist
        news_data = response.json()
        return news_data
    except requests.exceptions.RequestException as e:
        print(f"HTTP-Fehler: {e}")
    except requests.exceptions.JSONDecodeError as e:
        print(f"JSON-Fehler: {e}")
        return None
    # Beispielaufruf
    news = fetch_news()
    if news:
        print(news)
    else:
        print("Keine Nachrichten gefunden oder Fehler beim Abrufen der Nachrichten.")

    
# rag the llama model for generating news
def rag_model():
    documents = [
        "Das ist ein Beispieltext für die erste Nachricht.",
        "Hier ist ein weiterer Beispieltext für die zweite Nachricht.",
    ]
    
    client = db.Client()
    collection = client.create_collection("news_collection")
    
    # save each document in a vector-embedding-database 
    # translate every document into a vector embedding
    # and save it in the database
    for i, d in enumerate(documents):
        response = lama.embed(model="mxbai-embed-large", input=d)
        embeddings = response["embeddings"]
        collection.add(
            ids=[str(i)],
            embeddings=embeddings,
            documents=[d],
        )
    
    print("Documents added to the database.")

def start_game():
    print("Game started!")
    fetch_news()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    root.destroy()

    game_window = tk.Tk()
    game_window.title("Game Window")
    game_window.geometry(f"{screen_width}x{screen_height}")
    game_window.configure(bg="#f0f4f7")  # heller Hintergrund

    # -------------- Hauptstruktur -----------------
    main_frame = tk.Frame(game_window, bg="#f0f4f7")
    main_frame.pack(fill="both", expand=True)

    # news title
    title_label = tk.Label(
        main_frame,
        text="News Titel kommt hier hin",
        font=("Helvetica", 32, "bold"),
        bg="#f0f4f7",
        fg="#333",
        wraplength=800,
        justify="center"
    )
    title_label.pack(pady=40)

    # news content
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

    # buttons for real and fake
    buttons_frame = tk.Frame(main_frame, bg="#f0f4f7")
    buttons_frame.pack(side="bottom", pady=50)

    button_style = {
        "font": ("Helvetica", 24, "bold"),
        "width": 12,
        "height": 2,
        "bg": "#4CAF50",       # Grün
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
    fake_button_style["bg"] = "#f44336"          # Rot
    fake_button_style["activebackground"] = "#e53935"

    fake_button = tk.Button(buttons_frame, text="Fake", **fake_button_style)
    fake_button.grid(row=0, column=1, padx=50, pady=20)

    game_window.mainloop()

# Start-Fenster
root = tk.Tk()
root.title("Get the fake")
root.geometry("300x250")
root.configure(bg="#f0f4f7")  # gleicher heller Hintergrund

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
    command=start_game,
    font=("Helvetica", 14, "bold"),
    bg="#2196F3",            # Blau
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
