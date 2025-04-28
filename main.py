import tkinter as tk
import ollama as lama
import chromadb as db
import requests
import random
import urllib.parse


# ------------- HELPERS ------------------
def random_number(x):
    return random.randint(0, x)


# --------------API HANDLING ------------------
# get news from tagesschau.de
def fetch_news():
    jsonData = []
    ressorts = ["inland", "ausland", "wirtschaft", "sport", "video", "investigativ", "wissen"]
    baseUrl = "https://www.tagesschau.de/api2u/news/"
    url = f"{baseUrl}?regions={random_number(15)+1}&ressort={ressorts[random_number(len(ressorts) - 1)]}"
    
    # encode the URL to ensure it is valid
    url = urllib.parse.quote(url, safe=':/?=&')
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # check for HTTP errors
        news_data = response.json()
        
        # check if the response is in the expected format
        if isinstance(news_data, dict) and 'news' in news_data:
            for news in news_data['news']:
                title = news.get("title", "Kein Titel verfügbar")
                jsonData.append({"title": title})
            return jsonData
        else:
            print("Unerwartetes JSON-Format")
            return None
    except requests.exceptions.RequestException as e:
        print(f"HTTP-Fehler: {e}")
    except requests.exceptions.JSONDecodeError as e:
        print(f"JSON-Fehler: {e}")
        return None

#----------------- DIALOG HANDLER ------------------
# RAG-Model for the news generation with llama
def rag_model(news_data):
    client = db.Client()
    collection = client.create_collection("news_collection")
    
    # save every tite in the database
    for i, news in enumerate(news_data):
        title = news["title"]
        response = lama.embed(model="mxbai-embed-large", input=title)
        embeddings = response["embeddings"]
        collection.add(
            ids=[str(i)],
            embeddings=embeddings,
            documents=[title],
        )
    print("Titles added to the database.")
    return collection

def get_a_news(collection, default_prompt):
    response = lama.embed(model="mxbai-embed-large", input=default_prompt)
    embedding = response["embeddings"]
    if not embedding:
            raise ValueError("Die Einbettung ist leer. Überprüfe die Eingabe für die Einbettung.")
    
    results = collection.query(
        query_embeddings=embedding,
        n_results=1,
    )
    print(results)
    relevant_titles = [result[0] for result in results["documents"]]
    prompt= f"{default_prompt} {relevant_titles[0]}"
    answer = lama.generate(
        model="llama2",
        prompt=prompt
    )
    return answer["response"]
#----------------- GAME ------------------
def start_game():
    print("Game started!")
    news_data = fetch_news()
    if news_data:
        collection = rag_model(news_data)
        file = open("default_prompt.txt", "r", encoding="utf-8")
        default_prompt =  file.read()
        print(default_prompt)
        file.close()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        root.destroy()

        game_window = tk.Tk()
        game_window.title("Game Window")
        game_window.geometry(f"{screen_width}x{screen_height}")
        game_window.configure(bg="#f0f4f7")

        main_frame = tk.Frame(game_window, bg="#f0f4f7")
        main_frame.pack(fill="both", expand=True)

        # news title
        title_label = tk.Label(
            main_frame,
            text=get_a_news(collection=collection, default_prompt=default_prompt),  # set title from the first news item
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

        # real or fake buttons
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
    else:
        print("Fehler beim Abrufen der Nachrichten.")

# start the main window
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
    command=start_game,
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
