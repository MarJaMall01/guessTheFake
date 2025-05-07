import ollama as lama
import chromadb as db
import random
import time

def rag_model(news_data):
    client = db.Client()
    collection = client.create_collection("news_collection")

    titles = [news["title"] for news in news_data]
    response = lama.embed(model="mxbai-embed-large", input=titles)
    embeddings = response["embeddings"]
    ids = [str(i) for i in range(len(titles))]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=titles,
    )
    print("Titles added to the database.")
    return collection

def get_a_news(collection, default_prompt):
    response = lama.embed(model="mxbai-embed-large", input=default_prompt)
    embedding = response["embeddings"]
    if not embedding:
        raise ValueError("Die Einbettung ist leer.")

    results = collection.query(query_embeddings=embedding, n_results=3)
    relevant_titles = [doc[0] for doc in results["documents"]]
    selected_title = random.choice(relevant_titles)

    prompt = f"{default_prompt} {selected_title}"
    start = time.time()
    answer = lama.generate(
        model="llama2-uncensored",
        prompt=prompt,
        system=default_prompt
    )
    print(f"Antwort generiert in {time.time() - start:.2f} Sekunden")
    return answer["response"]
