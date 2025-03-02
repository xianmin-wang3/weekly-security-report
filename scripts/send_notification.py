import requests
import os

# 讀取環境變數
LINE_NOTIFY_TOKEN = os.getenv("LINE_NOTIFY_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # GitHub API Token
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")
GITHUB_RUN_ID = os.getenv("GITHUB_RUN_ID")
GITHUB_ARTIFACT_ID = os.getenv("GITHUB_ARTIFACT_ID")

# GitHub API 下載 Artifact URL
GITHUB_ARTIFACT_URL = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/actions/artifacts/{GITHUB_ARTIFACT_ID}"

# 下載檔案
def download_artifact():
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    response = requests.get(GITHUB_ARTIFACT_URL, headers=headers)

    if response.status_code == 200:
        with open("security_report.zip", "wb") as f:
            f.write(response.content)
        print("✅ 成功下載 security-report.zip")
        return "security_report.zip"
    else:
        print(f"❌ 下載 Artifact 失敗: {response.status_code}, {response.text}")
        return None

# 發送 LINE 通知
def send_line_notify(file_path):
    if not LINE_NOTIFY_TOKEN:
        print("❌ 錯誤: 未設定 LINE_NOTIFY_TOKEN 環境變數")
        return

    # 設定 HTTP 標頭
    headers = {
        "Authorization": f"Bearer {LINE_NOTIFY_TOKEN}"
    }

    # 設定訊息
    message = f"📢 資安新聞週報 📢\n\n最新資安新聞已整理完成！\n📂 附件下載：GitHub Artifact"

    # 準備檔案發送
    files = {"file": open(file_path, "rb")}
    data = {"message": message}

    # 發送請求
    response = requests.post("https://notify-api.line.me/api/notify", headers=headers, data=data, files=files)

    # 檢查回應
    if response.status_code == 200:
        print("✅ 訊息與檔案已成功發送至 LINE！")
    else:
        print(f"❌ LINE Notify 發送失敗，錯誤碼: {response.status_code}, 錯誤訊息: {response.text}")

if __name__ == "__main__":
    file_path = download_artifact()
    if file_path:
        send_line_notify(file_path)

