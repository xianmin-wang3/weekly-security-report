import requests
import os

LINE_NOTIFY_TOKEN = os.getenv("LINE_NOTIFY_TOKEN")

def send_line_notification():
    if not LINE_NOTIFY_TOKEN:
        print("❌ LINE_NOTIFY_TOKEN 未設定，請確認 GitHub Secrets 設置正確！")
        return

    message = "資安週報已更新！請查看最新簡報 📄"
    pdf_url = "https://raw.githubusercontent.com/gary125/weekly-security-report/main/data/report.md"

    headers = {"Authorization": f"Bearer {LINE_NOTIFY_TOKEN}"}
    data = {"message": f"{message}\n{pdf_url}"}

    response = requests.post("https://notify-api.line.me/api/notify", headers=headers, data=data)

    if response.status_code == 200:
        print("✅ LINE 通知已成功發送！")
    else:
        print(f"❌ 發送失敗，錯誤碼：{response.status_code}, 回應內容：{response.text}")

if __name__ == "__main__":
    send_line_notification()
