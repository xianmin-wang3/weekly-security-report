import os
import json
import re

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

    markdown_content = """---
marp: true
theme: gaia
paginate: true
---

# 📢 資安新聞週報

每週精選最新資安新聞摘要 🚀
"""

    for news in summaries:
        title = re.sub(r"[#*_`$begin:math:display$$end:math:display$]", "", news["title"])  # 過濾 Markdown 特殊字元
        summary = news["summary"]
        link = news["link"]

        markdown_content += f"""
---

## 📰 {title}

{summary}

📎 [閱讀更多]({link})

"""

    os.makedirs(os.path.dirname(MARKDOWN_FILE), exist_ok=True)
    with open(MARKDOWN_FILE, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    print(f"✅ 已成功生成 Marp 簡報: {MARKDOWN_FILE}")

if __name__ == "__main__":
    generate_marp_slides()