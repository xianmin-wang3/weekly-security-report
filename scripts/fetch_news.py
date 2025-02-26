import os
import json
import requests
from bs4 import BeautifulSoup

# iThome 資安新聞頁面 URL
ITHOME_URL = "https://www.ithome.com.tw/tags/資安"
NEWS_FILE = "data/news.json"  # 存儲新聞的 JSON 檔案

def fetch_news_content(url):
    """從新聞連結抓取完整文章內容"""
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()  # 檢查請求是否成功
        soup = BeautifulSoup(response.text, "html.parser")

        content_div = soup.find("div", class_="field-items")
        if content_div:
            paragraphs = content_div.find_all("p")
            content = "\n".join(p.text.strip() for p in paragraphs if p.text.strip())
            print(f"🔍 抓取內容長度: {len(content)} 字")
            return content

        print(f"⚠️ 未能抓取完整內容: {url}")
        return "❌ 無法獲取完整新聞內容"

    except Exception as e:
        print(f"⚠️ 抓取新聞內容錯誤: {e}")
        return "❌ 發生錯誤，請稍後再試"

def fetch_news():
    """抓取 iThome 最新 5 篇資安新聞"""
    response = requests.get(ITHOME_URL, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    news_items = soup.find_all("div", class_="view-list-item", limit=5)  # 只抓取最新 5 篇
    news_list = []

    for item in news_items:
        a_tag = item.find("a")
        if not a_tag:
            continue

        title = a_tag.text.strip()
        link = "https://www.ithome.com.tw" + a_tag["href"]
        content = fetch_news_content(link)  # 取得完整新聞內容

        news_list.append({"title": title, "link": link, "content": content})
        print(f"✅ 已抓取: {title}")

    os.makedirs(os.path.dirname(NEWS_FILE), exist_ok=True)
    with open(NEWS_FILE, "w", encoding="utf-8") as f:
        json.dump(news_list, f, ensure_ascii=False, indent=4)

    print(f"✅ 所有新聞已儲存至 {NEWS_FILE}")

if __name__ == "__main__":
    fetch_news()