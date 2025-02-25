import os
import requests
import json
from groq import Groq

# 獲取 Groq API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 確保 API Key 存在
if not GROQ_API_KEY:
    raise ValueError("❌ 環境變數 GROQ_API_KEY 未設定！請檢查 GitHub Secrets 或 .env 檔案")

# 讀取新聞內容
NEWS_FILE = "data/news.json"  # 原始新聞檔案
SUMMARY_FILE = "data/summaries.json"  # 儲存摘要結果

def load_news():
    """ 讀取原始新聞資料 """
    if not os.path.exists(NEWS_FILE):
        raise FileNotFoundError(f"❌ 找不到新聞檔案: {NEWS_FILE}")
    
    with open(NEWS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def summarize_text(text):
    """ 使用 Groq API 總結新聞內容 """
    api_url = "https://api.groq.com/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-8b-8192",  # Groq API 模型
        "messages": [{"role": "user", "content": f"請用簡潔的方式總結這篇文章(使用繁體中文回答): {text}"}],
        "temperature": 0.5
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()  # 檢查是否有 HTTP 錯誤

        data = response.json()
        summary = data["choices"][0]["message"]["content"]
        print("✅ 成功獲取摘要")
        return summary

    except requests.exceptions.RequestException as e:
        print(f"❌ API 請求錯誤: {e}")
        return "無法獲取摘要"

def summarize_news():
    """ 總結所有新聞內容 """
    news_data = load_news()
    summaries = []

    for article in news_data:
        title = article.get("title", "無標題")
        content = article.get("content", "")

        if not content:
            print(f"⚠️ 文章 {title} 沒有內容，跳過...")
            continue

        print(f"📄 總結文章: {title}")
        summary = summarize_text(content)

        summaries.append({
            "title": title,
            "summary": summary,
            "link": article.get("link", "#")  # 保留原始新聞連結
        })

    # 儲存摘要結果
    os.makedirs(os.path.dirname(SUMMARY_FILE), exist_ok=True)
    with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
        json.dump(summaries, f, ensure_ascii=False, indent=4)

    print(f"✅ 所有新聞摘要完成，已儲存至 {SUMMARY_FILE}")

if __name__ == "__main__":
    summarize_news()
