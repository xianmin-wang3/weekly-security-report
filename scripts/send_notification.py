import requests
import os

# 從環境變數讀取 LINE Notify Token
LINE_NOTIFY_TOKEN = os.getenv("LINE_NOTIFY_TOKEN")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")  # 自動獲取 repo 名稱
GITHUB_RUN_ID = os.getenv("GITHUB_RUN_ID")  # 取得當前 workflow run ID
GITHUB_ARTIFACT_URL = f"https://github.com/{GITHUB_REPOSITORY}/actions/runs/{GITHUB_RUN_ID}"

def send_line_notification():
    """發送 LINE Notify 通知，附上 PDF 簡報連結"""
    if not LINE_NOTIFY_TOKEN:
        print("❌ LINE_NOTIFY_TOKEN 未設定，請確認 GitHub Secrets 設置正確！")
        return

    message = "📢 資安週報已更新！請查看最新簡報 📄\n🔗 下載 PDF: " + GITHUB_ARTIFACT_URL

    headers = {"Authorization": f"Bearer {LINE_NOTIFY_TOKEN}"}
    data = {"message": message}

    response = requests.post("https://notify-api.line.me/api/notify", headers=headers, data=data)

    if response.status_code == 200:
        print("✅ LINE 通知已成功發送！")
    else:
        print(f"❌ 發送失敗，錯誤碼：{response.status_code}, 回應內容：{response.text}")

if __name__ == "__main__":
    send_line_notification()