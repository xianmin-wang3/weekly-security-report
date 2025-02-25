import requests
import os

LINE_NOTIFY_TOKEN = os.getenv("LINE_NOTIFY_TOKEN")

def send_line_notification():
    message = "資安週報已更新！請查看最新簡報 📄"
    pdf_url = "https://your-github-repo-url/data/report.pdf"

    headers = {"Authorization": f"Bearer {LINE_NOTIFY_TOKEN}"}
    data = {"message": f"{message}\n{pdf_url}"}

    response = requests.post("https://notify-api.line.me/api/notify", headers=headers, data=data)
    print("已發送 LINE 通知！")

if __name__ == "__main__":
    send_line_notification()
