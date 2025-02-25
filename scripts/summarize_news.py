import os
import json
import time
from groq import Groq

# 設定檔案路徑
NEWS_FILE = "data/news.json"  # 原始新聞 JSON 檔案
SUMMARY_FILE = "data/summaries.json"  # 總結結果 JSON 檔案

# 獲取 Groq API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 確保 API Key 存在
if not GROQ_API_KEY:
    raise ValueError("❌ 環境變數 GROQ_API_KEY 未設定！請檢查 GitHub Secrets 或 .env 檔案")

# 初始化 Groq 客戶端
client = Groq(api_key=GROQ_API_KEY)

def load_news():
    """讀取原始新聞資料"""
    if not os.path.exists(NEWS_FILE):
        raise FileNotFoundError(f"❌ 找不到新聞檔案: {NEWS_FILE}")
    
    with open(NEWS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def summarize_text(title, link):
    """使用 Groq API 總結新聞內容"""
    try:
        # 提示詞讓 Groq 直接從新聞連結生成摘要（如果網站允許）
        prompt = (
            f"請用繁體中文簡潔地總結這篇新聞文章:\n\n"
            f"標題: {title}\n"
            f"新聞連結: {link}\n"
            f"請提供 3-5 句的摘要，並保留新聞的重點內容。"
        )

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "你是個專業的新聞摘要助手，請提供簡明扼要的新聞摘要。"},
                {"role": "user", "content": prompt}
            ],
            model="llama3-70b",  # 確保 Groq 支援的模型
        )

        summary = chat_completion.choices[0].message.content.strip()
        print(f"✅ 總結完成: {title}")
        return summary

    except Exception as e:
        print(f"❌ API 請求錯誤 ({title}): {e}")
        return "無法獲取摘要"

def summarize_news():
    """總結所有新聞內容"""
    news_data = load_news()
    summaries = []

    for article in news_data:
        title = article.get("title", "無標題")
        link = article.get("link", "#")

        print(f"📄 總結文章: {title}")

        summary = summarize_text(title, link)
        summaries.append({"title": title, "summary": summary, "link": link})

        # 避免 API 請求過快導致限流
        time.sleep(2)  # 適當延遲以降低 API 請求頻率

    # 儲存摘要結果
    os.makedirs(os.path.dirname(SUMMARY_FILE), exist_ok=True)
    with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
        json.dump(summaries, f, ensure_ascii=False, indent=4)

    print(f"✅ 所有新聞摘要完成，已儲存至 {SUMMARY_FILE}")

if __name__ == "__main__":
    summarize_news()