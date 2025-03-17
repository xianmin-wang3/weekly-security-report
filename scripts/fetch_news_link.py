import os
import json
import requests
from bs4 import BeautifulSoup

# iThome 資安新聞頁面 URL
ITHOME_URL = "https://www.ithome.com.tw/tags/資安日報"
NEWS_FILE = "../data/news_links.json"  # 存儲新聞的 JSON 檔案

def fetch_news_links():
    """抓取 iThome 最新 5 篇資安新聞的連結"""
    try:
        response = requests.get(ITHOME_URL, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        news_items = soup.find("div", class_="view-content").find_all("div", class_="views-row", limit=3)
        news_list = []

        for item in news_items:
            a_tag = item.find("a")
            if not a_tag:
                continue

            link = a_tag["href"]
            if not link.startswith("http"):
                link = "https://www.ithome.com.tw" + link

            news_list.append({"link": link})  # 只保留 link
            print(f"✅ 已抓取連結: {link}")

        os.makedirs(os.path.dirname(NEWS_FILE), exist_ok=True)
        with open(NEWS_FILE, "w", encoding="utf-8") as f:
            json.dump(news_list, f, ensure_ascii=False, indent=4)

        print(f"✅ 所有新聞連結已儲存至 {NEWS_FILE}")

    except Exception as e:
        print(f"⚠️ 抓取新聞連結錯誤: {e}")

if __name__ == "__main__":
    fetch_news_links()
    
