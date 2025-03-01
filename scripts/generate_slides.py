import os
import json
import re

SUMMARY_FILE = "../data/summaries.json"
MARKDOWN_FILE = "../data/report.md"

def load_summary():
    """讀取 weekly_summary JSON"""
    if not os.path.exists(SUMMARY_FILE):
        raise FileNotFoundError(f"❌ 找不到摘要檔案: {SUMMARY_FILE}")

    with open(SUMMARY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def format_section(title, content):
    """格式化 Marp 幻燈片內容"""
    return f"""
---

## {title}

{content}
"""

def format_security_events(content):
    """格式化資安事件為 Markdown 清單"""
    # 1. 確保每個事件獨立一行（避免連續寫在一起）
    content = content.replace("。", "。\n")  

    # 2. 將「日期」前面加上 `- **` 來標示為 Markdown 清單
    content = re.sub(r"(\d{1,2}月\d{1,2}日)", r"\n- **\1**", content)

    # 3. 移除首尾多餘的換行符
    return content.strip()

def generate_marp_slides():
    """生成 Marp 簡報 Markdown 檔案"""
    summaries = load_summary()
    weekly_summary = summaries.get("weekly_summary", "")

    # 定義標題對應的正則表達式
    sections = {
        "資安防護": r"1\.\s\*\*(資安防護)\*\*：(.+?)(?=\n\n\d|$)",
        "資安威脅態勢": r"2\.\s\*\*(資安威脅態勢)\*\*：(.+?)(?=\n\n\d|$)",
        "資安事件": r"3\.\s\*\*(資安事件)\*\*：(.+?)(?=\n\n\d|$)",
        "未來趨勢": r"4\.\s\*\*(未來趨勢)\*\*：(.+)",
    }

    markdown_content = """---
marp: true
theme: gaia
paginate: true
---

# 📢 資安新聞週報

每週精選最新資安新聞摘要 🚀
"""

    # 解析並添加各部分內容
    for title, pattern in sections.items():
        match = re.search(pattern, weekly_summary, re.DOTALL)
        if match:
            content = match.group(2).strip()
            # 特殊處理「資安事件」，確保格式正確
            if title == "資安事件":
                content = format_security_events(content)

            markdown_content += format_section(f"📌 {title}", content)

    # 確保輸出目錄存在
    os.makedirs(os.path.dirname(MARKDOWN_FILE), exist_ok=True)
    
    with open(MARKDOWN_FILE, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    print(f"✅ 已成功生成 Marp 簡報: {MARKDOWN_FILE}")

if __name__ == "__main__":
    generate_marp_slides()
