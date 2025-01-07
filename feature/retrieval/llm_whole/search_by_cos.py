import requests
import json
import numpy as np
from qdrant_client import QdrantClient

def vectorize_user_question(question):
    """
    将用户输入的问题向量化
    """
    url = 'https://api.jina.ai/v1/embeddings'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer jina_6048b76532824efe82a449f8cd2b761bPvhOusuuPM-0GtWolcjrZb_XlvGx'
    }

    data = {
        "model": "jina-embeddings-v3",
        "task": "text-matching",
        "late_chunking": False,
        "dimensions": 1024,
        "embedding_type": "float",
        "input": [question]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        response_json = response.json()
        embedding = response_json["data"][0]["embedding"]
        return embedding
    else:
        print(f"请求失败，HTTP 状态码: {response.status_code}")
        print(response.text) 
        return None

def query_qdrant(client, collection_name, query_vector, top_k):
    """
    在 Qdrant 数据库中查询
    """
    try:
        hits = client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=top_k,
            with_payload=True,
        )
        
        for hit in hits:
            print(hit.payload, "score:", hit.score)
            

    except Exception as e:
        print(f"查询 Qdrant 失败: {e}")


def list_placeids(client, collection_name) -> list:
    """
    列出集合中的所有 placeid
    """
    try:
        placeids = []
        # 滚动查询所有数据
        scroll = client.scroll(collection_name=collection_name, with_payload=True)
        for point in scroll[0]:
            if 'file_name' in point.payload:
                placeids.append(point.payload['file_name'])

        return placeids

    except Exception as e:
        print(f"列出 placeid 失败: {e}")


if __name__ == "__main__":
    try:
        # 初始化 Qdrant 客户端

        client = QdrantClient("https://7ea5deab-8a79-4c4f-bbc3-edb3f5f98a03.us-east4-0.gcp.cloud.qdrant.io:6333",
        api_key="jPdSAiS9gE7xrk-gLA8NPqPkigvhr2uHfx1tQmdfGsV0eB3l2bP72A")
        collection_name = "example_collection"

        
        # 打印所有 placeid
        placeids = list_placeids(client, collection_name) 
        print("集合中的所有 file_name:", placeids)


        while True:
            question = input("请输入您的问题（输入 'q' 退出）：")
            if question.lower() == 'q':
                break

            embedding = vectorize_user_question(question)
            # print(embedding)    # 印出向量

            if embedding:
                print("嵌入向量成功生成，正在查询 Qdrant...")
                query_qdrant(client, collection_name, embedding, 5)
            else:
                print("嵌入向量生成失败，请重试！")
    except Exception as e:
        print(f"Qdrant 客户端初始化失败: {e}")
