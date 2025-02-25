import requests
from bs4 import BeautifulSoup
import json
import os

ITHOME_URL = "https://www.ithome.com.tw/tags/資安"

def fetch_ithome_news():
    """抓取 iThome 最新 5 篇資安新聞的標題、連結與完整內容"""
    try:
        response = requests.get(ITHOME_URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        response.raise_for_status()  # 確保 HTTP 回應碼為 200
    except requests.RequestException as e:
        print(f"⚠️ 請求失敗: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("div", class_="view-list-item")  # 找到所有新聞項目

    news_list = []
    for article in articles[:5]:  # 取得最新 5 篇新聞
        title_tag = article.find("a")  # 找到 <a> 標籤（標題與連結）
        title = title_tag.text.strip() if title_tag else "無標題"
        link = "https://www.ithome.com.tw" + title_tag["href"] if title_tag else "#"
        
        # 抓取文章完整內容
        content = fetch_news_content(link)

        news_list.append({"title": title, "link": link, "content": content})

        # 顯示抓取進度
        print(f"✅ 已抓取: {title}")

    return news_list

def fetch_news_content(url):
    """抓取 iThome 資安新聞的完整內容"""
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"⚠️ 無法取得文章內容 ({url}): {e}")
        return "無法獲取文章內容"

    soup = BeautifulSoup(response.text, "html.parser")
    
    # iThome 文章內容位於 <div class="field-items">
    content_div = soup.find("div", class_="field-items")
    
    if content_div:
        paragraphs = content_div.find_all("p")  # 找出所有 <p> 標籤的段落
        content = "\n".join(p.text.strip() for p in paragraphs if p.text.strip())  # 轉換成完整文章
        return content

    return "無法獲取文章內容"

if __name__ == "__main__":
    print("📡 正在抓取 iThome 資安新聞...")
    news = fetch_ithome_news()
    
    # 確保 data 目錄存在
    os.makedirs("data", exist_ok=True)
    
    # 存入 JSON 檔案
    with open("data/news.json", "w", encoding="utf-8") as f:
        json.dump(news, f, ensure_ascii=False, indent=2)
    
    print("🎉 已成功取得 iThome 資安新聞全文！")
    print("📄 JSON 檔案已儲存至 data/news.json")
