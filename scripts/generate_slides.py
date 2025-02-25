import os
import json

SUMMARY_FILE = "data/summaries.json"
MARKDOWN_FILE = "data/report.md"

def load_summaries():
    """讀取新聞摘要 JSON"""
    if not os.path.exists(SUMMARY_FILE):
        raise FileNotFoundError(f"❌ 找不到摘要檔案: {SUMMARY_FILE}")
    
    with open(SUMMARY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_marp_slides():
    """生成 Marp 簡報 Markdown 檔案"""
    summaries = load_summaries()

    # 簡報起始設定
    markdown_content = """---
marp: true
theme: gaia  # 可改為 uncover 風格
paginate: true
---

# 📢 資安新聞週報

每週精選最新資安新聞摘要 🚀
"""

    for news in summaries:
        title = news["title"].replace("#", "")  # 避免 Markdown 語法衝突
        summary = news["summary"]
        link = news["link"]

        markdown_content += f"""
---

## 📰 {title}

{summary}

📎 [閱讀更多]({link})

"""

    # 確保資料夾存在
    os.makedirs(os.path.dirname(MARKDOWN_FILE), exist_ok=True)

    # 儲存 Markdown 簡報
    with open(MARKDOWN_FILE, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    print(f"✅ 已成功生成 Marp 簡報: {MARKDOWN_FILE}")

if __name__ == "__main__":
    generate_marp_slides()