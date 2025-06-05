import requests
import urllib.parse
from utils import random_number

def flatten_article_content(content_field):
    if isinstance(content_field, list):
        return " ".join(block.get("value", "") for block in content_field if isinstance(block, dict))
    elif isinstance(content_field, str):
        return content_field
    return ""

def fetch_full_article(details_url):
    try:
        response = requests.get(details_url)
        response.raise_for_status()
        article_data = response.json()
        raw_content = article_data.get("content", "")
        return flatten_article_content(raw_content)
    except Exception as e:
        print(f"Fehler beim Abrufen von Artikelinhalt: {e}")
        return ""

def fetch_news():
    news_data = []
    ressorts = ["inland", "ausland", "wirtschaft", "sport", "video", "investigativ", "wissen"]
    base_url = "https://www.tagesschau.de/api2u/news/"
    url = f"{base_url}?regions={random_number(15)+1}&ressort={ressorts[random_number(len(ressorts) - 1)]}"
    url = urllib.parse.quote(url, safe=':/?=&')

    try:
        response = requests.get(url)
        response.raise_for_status()
        raw_data = response.json()

        if isinstance(raw_data, dict) and 'news' in raw_data:
            for news in raw_data['news']:
                title = news.get("title", "Kein Titel verfügbar")
                details_url = news.get("details")
                if details_url:
                    full_content = fetch_full_article(details_url)
                    if full_content:
                        news_data.append({
                            "title": title,
                            "content": full_content
                        })
            return news_data if news_data else None
        else:
            print("Unerwartetes JSON-Format")
            return None
    except requests.exceptions.RequestException as e:
        print(f"HTTP-Fehler: {e}")
        return None
