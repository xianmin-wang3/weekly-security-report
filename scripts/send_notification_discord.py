import requests
import os

# 讀取環境變數
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
MARKDOWN_FILE = "../data/report.md"

def send_discord_message():
    if not DISCORD_WEBHOOK_URL:
        print("❌ 錯誤: 未設定 DISCORD_WEBHOOK_URL 環境變數")
        return

    if not os.path.exists(MARKDOWN_FILE):
        print(f"❌ 錯誤: 檔案不存在: {MARKDOWN_FILE}")
        return

    # 讀取 Markdown 內容
    with open(MARKDOWN_FILE, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    # Discord 單則訊息限制 2000 字，超過就截斷
    if len(markdown_content) > 2000:
        markdown_content = markdown_content[:1997] + "..."

    # 設定要發送的訊息
    payload = {
        "content": f"{markdown_content}"
    }

    # 發送到 Discord Webhook
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)

    # 檢查回應
    if response.status_code == 204:
        print("✅ 訊息已成功發送至 Discord！")
    else:
        print(f"❌ Discord 發送失敗，錯誤碼: {response.status_code}, 錯誤訊息: {response.text}")

if __name__ == "__main__":
    send_discord_message()
