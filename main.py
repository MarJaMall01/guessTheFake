import tkinter as tk
from tkinter import ttk
import ollama as lama
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

INDEX_PATH = "faiss.index"
TEXTS_PATH = "texts.npy"
# vector transforming via sentecetransformer and faiss
model = SentenceTransformer('all-MiniLM-L6-v2')

def getDocuments(path):
    examples = []
    for filename in os.listdir(path):
        if filename.endswith(".txt"):
            with open(os.path.join(path, filename), "r", encoding="utf-8") as f:
                text = f.read()
                examples.append(text)
    return examples

if os.path.exists(INDEX_PATH) and os.path.exists(TEXTS_PATH):
    index = faiss.read_index(INDEX_PATH)
    texts = np.load(TEXTS_PATH, allow_pickle=True).tolist()
else:
    docs = getDocuments("documents")

    # split the text in 500 letters per chunk+
    def chunkText(text, chunkSize=500):
        return [text[i:i+chunkSize] for i in range(0, len(text), chunkSize)]

    texts = []
    for doc in docs:
        chunk = chunkText(doc)
        texts.extend(chunk)

    embeddings = model.encode(texts, batch_size=32, show_progress_bar=True)

    #build index with faiss 
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))
    
    faiss.write_index(index, INDEX_PATH)
    np.save(TEXTS_PATH, texts)


#function to search in index
def search(query, k=3):
    queryVec = model.encode([query])
    distances, indices = index.search(queryVec, k)
    results = [texts[idx] for idx in indices[0]]
    return results

# llm via ollama 
def generateFakeNews(title, message, temperature=0.7, contextK = 3):
    with open("default_prompt.txt", "r", encoding="utf-8") as f:
        systemPrompt= f.read()
        
    #get context out of document chunks
    contextChunks = search(message, k=contextK)
    context = "\n\n".join(contextChunks)
    userPrompt = f"Titel der echten Nachricht: {title}\nInhalt der echten Nachricht: {message}\n\nKontext (das sind für dich hilfreiche Dokumente zur Erstellung von guten Fake News):\n{context}"
    print(systemPrompt)
    print(userPrompt)
    response = lama.chat(
        model='mistral',
        messages=[
            {"role": "system", "content": systemPrompt},
            {"role": "user", "content": userPrompt}
        ],
        options={"temperature": temperature}
    )
    return response['message']['content']

def showText():
    title = inputTitle.get("1.0", tk.END).strip()
    message = inputField.get("1.0", tk.END).strip()
    temperature = tempVar.get()
    contextK = contextVar.get()
    fakeNews = generateFakeNews(title, message, temperature, contextK)
    outputLbl.config(text=fakeNews)

# === colors and style ===
BG_COLOR = "#1e1e1e"
FRAME_COLOR = "#2d2d2d"
TEXT_COLOR = "#ffffff"
ACCENT_COLOR = "#0078d4"

# === window ===
root = tk.Tk()
root.title("Get a Fake!")

screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
root.geometry(f"{screenWidth}x{screenHeight}")
root.configure(bg=BG_COLOR)

# === STYLE AREA ===
style = ttk.Style()
style.theme_use("clam")  

# Hintergrundfarbe für Frames und Buttons
style.configure("TFrame", background=BG_COLOR)
style.configure("TButton",
                background=ACCENT_COLOR,
                foreground="white",
                font=("Segoe UI", 11),
                padding=6)
style.map("TButton",
          background=[("active", "#005a9e")])

# === LAYOUT AREA ===
mainFrame = ttk.Frame(root, padding=20)
mainFrame.pack(fill=tk.BOTH, expand=True)

inputFrame = ttk.Frame(mainFrame)
inputFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

## input fields and buttons
inputTitle = tk.Text(inputFrame, height=2, width=40, bg=FRAME_COLOR,
                     fg=TEXT_COLOR, font=("Segoe UI", 12), insertbackground="white", wrap="word", borderwidth=0)
inputTitle.insert("1.0", "Titel hier eingeben...")
inputTitle.pack(pady=(0, 10), padx=10)


inputField = tk.Text(inputFrame, height=15, width=40, bg=FRAME_COLOR,
                     fg=TEXT_COLOR, font=("Segoe UI", 12), insertbackground="white", wrap="word", borderwidth=0)
inputField.pack(pady=(0, 10), padx=10)


insertButton = ttk.Button(inputFrame, text="Generieren", command=showText)
insertButton.pack(pady=10, padx=10)

## output fields
outputFrame = ttk.Frame(mainFrame)
outputFrame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

outputLbl = tk.Label(outputFrame, text="", bg=FRAME_COLOR,
                     fg=TEXT_COLOR, anchor="nw", justify="left",
                     font=("Segoe UI", 12), wraplength=screenWidth//2, padx=10, pady=10)
outputLbl.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

## sliders
tempLbl = tk.Label(inputFrame, text="Halluzinationsgrad", bg=BG_COLOR, fg=TEXT_COLOR, font=("Segoe UI",10))
tempLbl.pack(pady=(10,0), padx=10, anchor="w")
tempVar = tk.DoubleVar(value=0.7)
tempSlider= tk.Scale(inputFrame, from_ = 0.2, to=1.0, resolution=0.1, orient="horizontal", variable=tempVar, bg=FRAME_COLOR, fg=TEXT_COLOR, highlightbackground=FRAME_COLOR, troughcolor=ACCENT_COLOR)
tempSlider.pack(padx=10, fill="x")

contextLbl = tk.Label(inputFrame, text="Kontext-Chunks", bg=BG_COLOR, fg=TEXT_COLOR, font=("Segoe UI",10))
contextLbl.pack(pady=(10,0), padx=10, anchor="w")
contextVar = tk.IntVar(value=3)
contextSlider = tk.Scale(inputFrame, from_=1, to=10, orient="horizontal", variable=contextVar, bg=FRAME_COLOR, fg=TEXT_COLOR, highlightbackground=FRAME_COLOR, troughcolor=ACCENT_COLOR)
contextSlider.pack(padx=10, fill="x")

root.mainloop()
