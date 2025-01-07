from langchain_openai import ChatOpenAI
from dotenv import dotenv_values
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# 加載環境變量
config = dotenv_values("./.env")

# 初始化 OpenAI 模型
llm = ChatOpenAI(
    model="gpt-4",
    openai_api_key=config.get("chat_gpt_key")
)

def extract_topics(reviews):
    """
    提取評論中的主要話題或集體意識
    :param reviews: 字符串列表，每條為一則評論
    :return: 主要話題及代表性評論
    """
    # 步驟 1：生成評論嵌入向量
    print("正在生成嵌入向量...")
    embeddings = []
    for review in reviews:
        response = llm.invoke(f"生成以下評論的嵌入向量：{review}")
        embeddings.append(np.array(response.content))  # 假設返回的嵌入是數字列表

    # 步驟 2：聚類分析
    print("正在進行聚類分析...")
    num_clusters = 5  # 假設聚類成 5 類
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(embeddings)
    labels = kmeans.labels_

    # 步驟 3：篩選高頻話題及代表性評論
    print("正在提取代表性評論...")
    topics = {}
    for cluster in range(num_clusters):
        cluster_reviews = [reviews[i] for i in range(len(labels)) if labels[i] == cluster]
        topics[f"話題 {cluster + 1}"] = cluster_reviews[:3]  # 提取每類的前三條評論

    return topics

if __name__ == "__main__":
    # 測試評論數據
    reviews = [
        "這家餐廳的氣氛很好，燈光很柔和。",
        "服務員態度很棒，非常細心。",
        "食物非常美味，尤其是牛排。",
        "環境很乾淨，但桌子有點擁擠。",
        "等餐時間過長，感覺有點不滿意。",
        "菜單選擇多樣，但價格偏高。",
        "甜點非常出色，是我吃過最好的一次。",
        "服務態度一般，有時候需要催促服務。",
        "整體氛圍很好，適合家庭聚餐。",
        "飲料選擇豐富，但味道普通。"
    ]

    topics = extract_topics(reviews)
    print("集體意識話題提取結果：\n")
    for topic, sample_reviews in topics.items():
        print(f"{topic}:")
        for review in sample_reviews:
            print(f"- {review}")
        print()
