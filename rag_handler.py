import ollama as lama
import chromadb as db
import random
import time

def flatten_article_content(content_field):
    if isinstance(content_field, list):
        return " ".join(block.get("value", "") for block in content_field if isinstance(block, dict))
    elif isinstance(content_field, str):
        return content_field
    return ""

def rag_model(news_data):
    client = db.Client()
    collection = client.create_collection("news_collection")

    documents = []
    titles = []
    ids = []

    for i, news in enumerate(news_data):
        title = news.get("title", "Kein Titel")
        raw_content = news.get("content", "")

        content = flatten_article_content(raw_content)
        if not content.strip():
            continue

        documents.append(content)
        titles.append(title)
        ids.append(str(i))

    response = lama.embed(model="mxbai-embed-large", input=documents)
    embeddings = response["embeddings"]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=[{"title": t} for t in titles]
    )

    print(f"{len(documents)} Artikel verarbeitet.")
    return collection

def get_a_news(collection, default_prompt):
    response = lama.embed(model="mxbai-embed-large", input=default_prompt)
    embedding = response["embeddings"]
    if not embedding:
        raise ValueError("Die Einbettung ist leer.")

    results = collection.query(query_embeddings=embedding, n_results=3)
    relevant_docs = [doc[0] for doc in results["documents"]]
    selected_doc = random.choice(relevant_docs)
    prompt = f"{default_prompt}\n\nOriginalinhalt:\n{selected_doc}"

    start = time.time()
    answer = lama.generate(
        model="llama3.2",
        prompt=prompt,
        system=default_prompt
    )
    print(f"Antwort generiert in {time.time() - start:.2f} Sekunden")
    return answer["response"]