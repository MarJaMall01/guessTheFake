import requests
import random
import urllib.parse
from utils import random_number

def fetch_news():
    jsonData = []
    ressorts = ["inland", "ausland", "wirtschaft", "sport", "video", "investigativ", "wissen"]
    baseUrl = "https://www.tagesschau.de/api2u/news/"
    url = f"{baseUrl}?regions={random_number(15)+1}&ressort={ressorts[random_number(len(ressorts) - 1)]}"
    url = urllib.parse.quote(url, safe=':/?=&')

    try:
        response = requests.get(url)
        response.raise_for_status()
        news_data = response.json()

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
