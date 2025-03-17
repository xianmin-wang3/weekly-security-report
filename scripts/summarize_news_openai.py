import os
import json
from openai import OpenAI

# 環境變數讀取 API 金鑰
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("❌ 環境變數 OPENAI_API_KEY 未設定！請檢查 GitHub Secrets 或 .env 檔案")

# 初始化 OpenAI 客戶端
client = OpenAI(api_key=OPENAI_API_KEY)

NEWS_FILE = "../data/security_news.json"
REPORT_FILE = "../data/report_openai.md"

def load_news():
    """讀取原始新聞資料"""
    if not os.path.exists(NEWS_FILE):
        raise FileNotFoundError(f"❌ 找不到新聞檔案: {NEWS_FILE}")

    with open(NEWS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def summarize_all_news(news_data):
    """使用 OpenAI API 生成 Markdown 格式的資安周報"""
    try:
        # 整理新聞內容
        news_list = "\n\n".join(
            [
                f"**標題**: {article['title']}\n"
                f"**說明**: {article['summary']}\n"
                f"**發布時間**: {article['publish_date']}\n"
                f"**本日關注**: {', '.join(article.get('preface', []))}\n"
                f"**資安攻擊與威脅**: {', '.join(article.get('threats', []))}\n"
                f"**資安漏洞與修補**: {', '.join(article.get('vulnerabilities', []))}\n"
                f"**資安防護**: {', '.join(article.get('security_measures', []))}\n"
                for article in news_data
            ]
        )

        print(f"📝 傳送給 OpenAI API 的新聞字數: {len(news_list)}")

        prompt = f"""
        你是專業的資安新聞摘要助手，我手邊整理了一週的資安新聞(部分內容整理錯誤，請自行判斷分類)：
        {news_list}

        請依據以下面向，整理為**Markdown 格式**的完整且精準的資安週報：
        - **1. 資安防護**
        - **2. 資安威脅態勢** (請詳細說明資安漏洞)
        - **3. 資安事件** (請標註日期)
        - **4. 未來趨勢**

        **輸出格式範例**：
        # 本週資安周報
        ## 1. 資安防護
        - **[標題]**: 說明內容
        ## 2. 資安威脅態勢
        - **[標題]**: 說明內容
        ## 3. 資安事件
        - **[標題]**: 說明內容
        ## 4. 未來趨勢
        - **[標題]**: 說明內容

        請用繁體中文回答，確保資訊完整！
        """

        # 呼叫 OpenAI API
        completion = client.chat.completions.create(
            model="gpt-4o-mini",  # 使用 gpt-4o-mini
            messages=[
                {"role": "system", "content": "你是專業的資安新聞摘要助手，請按照要求整理資訊。"},
                {"role": "user", "content": prompt}
            ]
        )

        summary_md = completion.choices[0].message.content.strip()
        print("✅ 本週資安周報總結完成")
        return summary_md

    except Exception as e:
        print(f"❌ API 請求錯誤: {e}")
        return "# 資安周報\n\n⚠️ 無法獲取完整摘要，請檢查 API 狀況。"

def save_markdown_report(content):
    """儲存 Markdown 格式的資安周報"""
    os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ 本週資安周報已儲存至 {REPORT_FILE}")

def summarize_news():
    """讀取所有新聞，生成並儲存 Markdown 格式的資安週報"""
    news_data = load_news()

    print("📄 開始生成本週資安周報...")
    summary_md = summarize_all_news(news_data)

    save_markdown_report(summary_md)

if __name__ == "__main__":
    summarize_news()
