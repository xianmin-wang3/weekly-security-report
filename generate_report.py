import feedparser
import requests
import os
from datetime import datetime

# 設定 RSS 來源（這裡是 SecurityWeek 的 RSS）
RSS_URL = "https://www.securityweek.com/feed/"

# 從 GitHub Secrets 讀取 LINE Notify Token
LINE_NOTIFY_TOKEN = os.getenv("LINE_TOKEN")
LINE_NOTIFY_API = "https://notify-api.line.me/api/notify"

# 解析 RSS，取得最新 5 則新聞
def fetch_news():
    feed = feedparser.parse(RSS_URL)
    news_list = []
    for entry in feed.entries[:5]:  # 取最新 5 則新聞
        news_list.append(f"🔹 {entry.title}\n🔗 {entry.link}")
    return news_list

# 產生 Markdown 格式的週報
def generate_report(news_list):
    today = datetime.now().strftime("%Y-%m-%d")
    report_content = f"# 資安週報 ({today})\n\n"
    for news in news_list:
        report_content += f"{news}\n\n"

    # 存成 Markdown 檔案
    with open("weekly_report.md", "w", encoding="utf-8") as f:
        f.write(report_content)
    
    return report_content

# 發送 LINE Notify 通知
def send_line_notify(message):
    headers = {"Authorization": f"Bearer {LINE_NOTIFY_TOKEN}"}
    data = {"message": message}
    response = requests.post(LINE_NOTIFY_API, headers=headers, data=data)
    print("已發送 LINE 通知" if response.status_code == 200 else "發送失敗")

if __name__ == "__main__":
    news_list = fetch_news()
    report = generate_report(news_list)
    send_line_notify("本週資安週報已產生 📢\n" + "\n".join(news_list[:3]))  # 只發前 3 則
