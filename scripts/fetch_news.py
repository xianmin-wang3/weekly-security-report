import requests
from bs4 import BeautifulSoup
import json

ITHOME_URL = "https://www.ithome.com.tw/tags/資安"

def fetch_ithome_news():
    response = requests.get(ITHOME_URL, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code != 200:
        print("無法取得 iThome 新聞")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("div", class_="view-list-item")

    news_list = []
    for article in articles[:5]:  # 取得最新 5 篇新聞
        title = article.find("a").text.strip()
        link = "https://www.ithome.com.tw" + article.find("a")["href"]
        news_list.append({"title": title, "link": link})

    return news_list

if __name__ == "__main__":
    news = fetch_ithome_news()
    with open("data/news.json", "w", encoding="utf-8") as f:
        json.dump(news, f, ensure_ascii=False, indent=2)
    print("已成功獲取 iThome 資安新聞！")
