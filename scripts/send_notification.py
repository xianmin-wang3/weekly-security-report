import requests
import os

# 讀取環境變數中的 LINE Notify Token
LINE_NOTIFY_TOKEN = os.getenv("LINE_NOTIFY_TOKEN")

# 你的 GitHub Pages PDF 連結（請替換為你的 repo）
GITHUB_PAGES_URL = "https://gary125.github.io/weekly-security-report/data/security_report.pdf"

def send_line_notify():
    if not LINE_NOTIFY_TOKEN:
        print("❌ 錯誤: 未設定 LINE_NOTIFY_TOKEN 環境變數")
        return
    
    headers = {
        "Authorization": f"Bearer {LINE_NOTIFY_TOKEN}"
    }

    message = f"📢 資安新聞週報 📢\n\n最新資安新聞已整理完成！\n📄 下載 PDF 週報：{GITHUB_PAGES_URL}"

    data = {"message": message}

    response = requests.post("https://notify-api.line.me/api/notify", headers=headers, data=data)

    if response.status_code == 200:
        print("✅ 訊息已成功發送至 LINE！")
    else:
        print(f"❌ LINE Notify 發送失敗，錯誤碼: {response.status_code}, 錯誤訊息: {response.text}")

if __name__ == "__main__":
    send_line_notify()
