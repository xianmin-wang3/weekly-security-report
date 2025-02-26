import os
import requests
from pdf2image import convert_from_path

# 讀取環境變數
LINE_NOTIFY_TOKEN = os.getenv("LINE_NOTIFY_TOKEN")
PDF_FILE_PATH = "data/security_report.pdf"  # PDF 簡報檔案
PDF_URL = "https://gary125.github.io/weekly-security-report/security_report.pdf"  # GitHub Pages URL
IMAGE_FILE_PATH = "data/security_report.png"  # 轉換後的圖片檔案（僅取第一頁）

def convert_pdf_to_image(pdf_path, output_image_path):
    """將 PDF 簡報的第一頁轉換為 PNG 圖片"""
    try:
        images = convert_from_path(pdf_path, dpi=200)  # 解析度 200 DPI
        if images:
            images[0].save(output_image_path, "PNG")  # 只儲存第一頁作為預覽
            print(f"✅ PDF 第一頁已轉換為圖片: {output_image_path}")
            return True
        else:
            print("❌ 無法轉換 PDF，未找到任何頁面！")
            return False
    except Exception as e:
        print(f"❌ PDF 轉圖片失敗: {e}")
        return False

def send_line_notification():
    """發送 LINE Notify 通知，附帶簡報圖片"""
    
    # 1️⃣ 確保環境變數設定正確
    if not LINE_NOTIFY_TOKEN:
        print("❌ LINE_NOTIFY_TOKEN 未設定，請確認 GitHub Secrets 設置正確！")
        exit(1)

    # 2️⃣ 檢查 PDF 是否存在
    if not os.path.exists(PDF_FILE_PATH):
        print(f"⚠️ 找不到 PDF 檔案 ({PDF_FILE_PATH})，通知將繼續發送但無法顯示簡報圖片！")

    # 3️⃣ 轉換 PDF 為圖片（僅第一頁）
    if os.path.exists(PDF_FILE_PATH):
        success = convert_pdf_to_image(PDF_FILE_PATH, IMAGE_FILE_PATH)
    else:
        success = False

    # 4️⃣ 設定通知訊息
    message = f"📢 資安週報已更新！\n請查看最新簡報：\n{PDF_URL}"

    headers = {"Authorization": f"Bearer {LINE_NOTIFY_TOKEN}"}

    # 5️⃣ 若成功轉換圖片，則上傳圖片到 LINE Notify
    if success and os.path.exists(IMAGE_FILE_PATH):
        with open(IMAGE_FILE_PATH, "rb") as image_file:
            files = {"imageFile": image_file}
            data = {"message": message}
            response = requests.post("https://notify-api.line.me/api/notify", headers=headers, data=data, files=files)
    else:
        # 若無圖片，則只發送純文字通知
        data = {"message": message}
        response = requests.post("https://notify-api.line.me/api/notify", headers=headers, data=data)

    # 6️⃣ 檢查 LINE API 回應
    if response.status_code == 200:
        print("✅ LINE 通知已成功發送！")
    else:
        print(f"❌ 發送失敗，錯誤碼：{response.status_code}\n回應內容：{response.text}")

if __name__ == "__main__":
    send_line_notification()