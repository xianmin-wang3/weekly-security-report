import os
import json
from groq import Groq

NEWS_FILE = "../data/security_news.json"
SUMMARY_FILE = "../data/summaries.json"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("❌ 環境變數 GROQ_API_KEY 未設定！請檢查 GitHub Secrets 或 .env 檔案")

client = Groq(api_key=GROQ_API_KEY)

def load_news():
    """讀取原始新聞資料"""
    if not os.path.exists(NEWS_FILE):
        raise FileNotFoundError(f"❌ 找不到新聞檔案: {NEWS_FILE}")

    with open(NEWS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def summarize_all_news(news_data):
    """使用 Groq API 生成整週資安新聞摘要"""
    try:
        # 組合完整新聞內容
        news_list = "\n\n".join(
            [
                f"標題: {article['title']}\n說明: {article['summary']}\n"
                f"發布時間: {article['publish_date']}\n"
                f"本日關注: {', '.join(article.get('preface', []))}\n"
                f"資安攻擊與威脅: {', '.join(article.get('threats', []))}\n"
                f"資安漏洞與修補: {', '.join(article.get('vulnerabilities', []))}\n"
                f"資安防護: {', '.join(article.get('security_measures', []))}\n"
                for article in news_data
            ]
        )

        print(f"📝 傳送給 Groq API 的新聞字數: {len(news_list)}")

        prompt = f"""
        你是專業的資安新聞摘要助手，我手邊整理了一週的資安新聞：
        {news_list}

        請依據以下面向，彙整出完整的資安週報：(務必記得編號，範例:1. **資安防護**)
        1. 資安防護
        2. 資安威脅態勢
        3. 資安事件 (若有日期請標註)
        4. 未來趨勢

        這很重要，請確保資訊完整，一步一步思考後再給出完整的週報內容，並確保用繁體中文回答。
        """

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "你是專業的資安新聞摘要助手，請按照要求整理資訊。"},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",
        )

        summary = chat_completion.choices[0].message.content.strip()
        print("✅ 本週資安周報總結完成")
        return summary

    except Exception as e:
        print(f"❌ API 請求錯誤: {e}")
        return "無法獲取資安周報摘要"

def summarize_news():
    """讀取所有新聞，生成整週資安新聞摘要"""
    news_data = load_news()

    print("📄 開始生成本週資安周報...")
    summary = summarize_all_news(news_data)

    summary_data = {"weekly_summary": summary}

    os.makedirs(os.path.dirname(SUMMARY_FILE), exist_ok=True)
    with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=4)

    print(f"✅ 本週資安周報已儲存至 {SUMMARY_FILE}")

if __name__ == "__main__":
    summarize_news()
