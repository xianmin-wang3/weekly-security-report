import os
import json
import pandas as pd
import requests
from bs4 import BeautifulSoup

# 讀取新聞鏈接
NEWS_FILE = "../data/news_links.json"
EXCEL_FILE = "../data/security_news.xlsx"
JSON_FILE = "../data/security_news.json"

def fetch_news_content(url):
    """抓取新聞詳細內容"""
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.find("h1", class_="page-header").text.strip() if soup.find("h1", class_="page-header") else "未知標題"
        summary = soup.find("div", class_="content-summary").text.strip() if soup.find("div", class_="content-summary") else "無摘要"
        publish_date = soup.find("span", class_="created").text.strip() if soup.find("span", class_="created") else "未知時間"
        
        # 初始化各個區域的內容 (改用字典存儲)
        sections = {
            "preface": "",
            "attack_threats": "",
            "vulnerabilities": "",
            "protection_measures": "",
            "recent_security_reports": ""
        }

        # 區塊對應標題
        section_map = {
            "攻擊與威脅": "attack_threats",
            "漏洞與修補": "vulnerabilities",
            "資安防禦措施": "protection_measures",
            "近期資安日報": "recent_security_reports"
        }

        # 抓取前言 & 主要新聞內容
        content_section = soup.select_one("div.field-name-body div.field-items")

        if not content_section:
            print(f"❌ {url} 無法找到主要新聞內容區塊")
            return None

        # 預設從 "前言" 開始
        current_section = "preface"

        # 遍歷所有 h3 & p
        for element in content_section.find_all(['h3', 'p']):
            if element.name == 'h3' and element.find('strong'):
                section_title = element.find('strong').text.strip('【】')
                print(f"🔍 偵測到標題: {section_title}")  # 測試是否正確擷取標題

                if section_title in section_map:
                    current_section = section_map[section_title]  # 更新當前區塊
                    print(f"✅ 切換至 {current_section}")  # 偵錯資訊

            elif element.name == 'p':
                content = element.get_text(strip=True)
                if content:
                    sections[current_section] += f"{content}"

        return {
            "title": title,
            "summary": summary,
            "publish_date": publish_date,
            "preface": sections["preface"],
            "attack_threats": sections["attack_threats"],
            "vulnerabilities": sections["vulnerabilities"],
            "protection_measures": sections["protection_measures"],
            "recent_security_reports": sections["recent_security_reports"],
            "link": url
        }

    except Exception as e:
        print(f"⚠️ 抓取新聞內容失敗: {e}")
        return None

def save_to_excel(news_data_list):
    """將爬取的新聞數據存入 Excel"""
    df = pd.DataFrame(news_data_list)
    df.to_excel(EXCEL_FILE, index=False, engine='openpyxl')
    print(f"✅ 成功保存到 Excel 文件: {EXCEL_FILE}")

def save_to_json(news_data_list):
    """將爬取的新聞數據存入 JSON"""
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(news_data_list, f, ensure_ascii=False, indent=4)
    print(f"✅ 成功保存到 JSON 文件: {JSON_FILE}")

def main():
    """主流程：讀取鏈接 -> 爬取內容 -> 存入 Excel 和 JSON"""
    if not os.path.exists(NEWS_FILE):
        print(f"⚠️ 找不到 {NEWS_FILE} 文件")
        return

    with open(NEWS_FILE, "r", encoding="utf-8") as f:
        news_links = json.load(f)

    news_data_list = []

    for news in news_links:
        url = news["link"]
        print(f"🔍 正在抓取: {url}")
        news_data = fetch_news_content(url)
        if news_data:
            news_data_list.append(news_data)

    if news_data_list:
        save_to_excel(news_data_list)
        save_to_json(news_data_list)

if __name__ == "__main__":
    main()
