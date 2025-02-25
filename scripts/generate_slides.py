import json

def generate_marp_slides():
    with open("data/summaries.json", "r", encoding="utf-8") as f:
        summaries = json.load(f)

    markdown_content = """
---
marp: true
theme: default
paginate: true
---

# 資安新聞週報

"""

    for news in summaries:
        markdown_content += f"""
---

## {news["title"]}

{news["summary"]}

[閱讀更多]({news["link"]})

"""

    with open("data/report.md", "w", encoding="utf-8") as f:
        f.write(markdown_content)

    print("已成功生成 Marp 簡報！")

if __name__ == "__main__":
    generate_marp_slides()
