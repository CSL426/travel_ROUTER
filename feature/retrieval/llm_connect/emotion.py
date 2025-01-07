from langchain_openai import ChatOpenAI
from dotenv import dotenv_values

# 加載環境變量
config = dotenv_values("./.env")

# 初始化 OpenAI 模型
llm = ChatOpenAI(
    model="GPT-4o mini",  # 可改為其他模型
    openai_api_key=config.get("chat_gpt_key")
)

# 定義情緒分析函數
def analyze_sentiment_with_score(review):
    """
    分析餐廳評論的情緒並以 1-10 分制呈現。
    :param review: 字符串格式的餐廳評論
    :return: 分數及解釋
    """
    prompt = f"""
    我希望你幫我分析以下餐廳評論的情緒，並以 1-10 分制進行評分：
    1 表示非常負面，10 表示非常正面，5 表示中性。
    同時，簡要解釋為什麼給出該分數。

    餐廳評論：{review}
    """
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"An error occurred: {e}"

# 主程式，用於測試多條評論
if __name__ == "__main__":
    # 測試評論
    reviews = [
        "這家餐廳的食物非常美味，服務非常友善。",
        "氣氛不錯，但食物偏鹹，價格也偏高。",
        "服務員態度很差，等了很久才上菜。",
    ]

    print("餐廳評論情緒分析及評分結果：\n")
    for i, review in enumerate(reviews, 1):
        print(f"評論 {i}: {review}")
        result = analyze_sentiment_with_score(review)
        print(f"分析結果：{result}\n")

