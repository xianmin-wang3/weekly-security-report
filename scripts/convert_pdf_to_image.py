from pdf2image import convert_from_path
import os

PDF_FILE = "data/security_report.pdf"
IMAGE_FILE = "data/security_report.png"

def convert_pdf_to_image(pdf_path, output_path):
    """將 PDF 第一頁轉為 PNG 圖片"""
    if not os.path.exists(pdf_path):
        print(f"❌ 找不到 PDF 檔案: {pdf_path}")
        return False

    try:
        images = convert_from_path(pdf_path, dpi=200)  # 解析度 200 DPI
        if images:
            images[0].save(output_path, "PNG")  # 儲存第一頁為 PNG
            print(f"✅ PDF 第一頁已轉換為圖片: {output_path}")
            return True
    except Exception as e:
        print(f"❌ PDF 轉圖片失敗: {e}")

    return False

if __name__ == "__main__":
    convert_pdf_to_image(PDF_FILE, IMAGE_FILE)
