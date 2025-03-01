import requests
import os

# 讀取環境變數中的 LINE Notify Token
LINE_NOTIFY_TOKEN = os.getenv("LINE_NOTIFY_TOKEN")

# 設定檔案路徑
file_path = '../data/security_report.pdf'

# 自動獲取 repo 名稱和 workflow run ID
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")
GITHUB_RUN_ID = os.getenv("GITHUB_RUN_ID")
GITHUB_ARTIFACT_URL = f"https://github.com/{GITHUB_REPOSITORY}/actions/runs/{GITHUB_RUN_ID}"

# LINE Notify API URL
url = "https://notify-api.line.me/api/notify"

def send_line_notify():
    if not LINE_NOTIFY_TOKEN:
        print("❌ 錯誤: 未設定 LINE_NOTIFY_TOKEN 環境變數")
        return

    if not os.path.exists(file_path):
        print("❌ 錯誤: 檔案不存在")
        return
    
    # 設定 HTTP 標頭
    headers = {
        "Authorization": f"Bearer {LINE_NOTIFY_TOKEN}"
    }

    # 設定訊息
    message = f"📢 資安新聞週報 📢\n\n最新資安新聞已整理完成！\n📄 下載 PDF 週報：{GITHUB_ARTIFACT_URL}"

    # 準備檔案發送
    files = {'file': open(file_path, 'rb')}
    data = {"message": message}

    # 發送請求
    response = requests.post(url, headers=headers, data=data, files=files)

    # 檢查回應
    if response.status_code == 200:
        print("✅ 訊息與檔案已成功發送至 LINE！")
    else:
        print(f"❌ LINE Notify 發送失敗，錯誤碼: {response.status_code}, 錯誤訊息: {response.text}")

if __name__ == "__main__":
    send_line_notify()
