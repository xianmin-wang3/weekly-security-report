import json
import openai
import os

# 設定 Groq API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
openai.api_key = GROQ_API_KEY

def summarize_news():
    with open("data/news.json", "r", encoding="utf-8") as f:
        news_list = json.load(f)

    summaries = []
    for news in news_list:
        title = news["title"]
        link = news["link"]
        
        prompt = f"請幫我總結以下新聞內容：\n標題：{title}\n連結：{link}\n\n摘要："
        
        response = openai.ChatCompletion.create(
            model="gpt-4", 
            messages=[{"role": "system", "content": "請用簡潔的方式摘要新聞內容。"},
                      {"role": "user", "content": prompt}]
        )

        summary = response["choices"][0]["message"]["content"]
        summaries.append({"title": title, "summary": summary, "link": link})

    with open("data/summaries.json", "w", encoding="utf-8") as f:
        json.dump(summaries, f, ensure_ascii=False, indent=2)

    print("已成功總結新聞！")

if __name__ == "__main__":
    summarize_news()
