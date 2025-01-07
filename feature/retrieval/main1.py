import os
import json
from llm_whole.search_filepath import total_file_path
from llm_whole.jina_control_number import embedding_jina
from llm_whole.qdrent_vector import QdrantClient
from llm_whole.search_by_cos import vectorize_user_question, query_qdrant
from llm_whole.clean_review import process_folder
import sys

# 將專案根目錄加入到 sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_path)

# 現在可以正確導入模組
from llm_whole.search_filepath import total_file_path

def clean_reviews():
    """
    清理餐廳評論 JSON 檔案，輸出清理後的文本
    """
    input_folder = r"./餐廳評論爬蟲1"  # 原始 JSON 資料夾
    output_folder = r"./cleaned_reviews"  # 清理後文本輸出資料夾

    print("開始清理評論...")
    process_folder(input_folder, output_folder)
    print("評論清理完成！")

def generate_embeddings():
    """
    為清理後的文本生成嵌入向量
    """
    cleaned_reviews_folder = r"./cleaned_reviews"  # 清理後的文本資料夾
    embedding_output_folder = r"./embedding_data"  # 嵌入向量儲存資料夾

    if not os.path.exists(embedding_output_folder):
        os.makedirs(embedding_output_folder)

    print("開始生成嵌入向量...")
    for file_name in os.listdir(cleaned_reviews_folder):
        if file_name.endswith(".txt"):
            file_path = os.path.join(cleaned_reviews_folder, file_name)
            restaurant_name = os.path.splitext(file_name)[0]
            embedding_jina(file_path, restaurant_name)
    print("嵌入向量生成完成！")

def upload_to_qdrant():
    """
    將嵌入向量上傳到 Qdrant 資料庫
    """
    print("開始上傳嵌入向量到 Qdrant...")
    client = QdrantClient(
        url="https://7ea5deab-8a79-4c4f-bbc3-edb3f5f98a03.us-east4-0.gcp.cloud.qdrant.io:6333",
        api_key="jPdSAiS9gE7xrk-gLA8NPqPkigvhr2uHfx1tQmdfGsV0eB3l2bP72A"
    )

    folder_path = "./embedding_data"
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".json"):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            vectors = [item["vector"] for item in data]
            payload = [{"file_name": os.path.splitext(file_name)[0], "text": item["text"]} for item in data]

            client.upload_collection(
                collection_name="example_collection",
                vectors=vectors,
                payload=payload
            )
    print("嵌入向量已成功上傳到 Qdrant！")

def search_qdrant():
    """
    提供查詢功能，使用者輸入問題並查詢 Qdrant 資料庫
    """
    print("開始查詢功能...")
    client = QdrantClient(
        url="https://7ea5deab-8a79-4c4f-bbc3-edb3f5f98a03.us-east4-0.gcp.cloud.qdrant.io:6333",
        api_key="jPdSAiS9gE7xrk-gLA8NPqPkigvhr2uHfx1tQmdfGsV0eB3l2bP72A"
    )
    collection_name = "example_collection"

    while True:
        question = input("請輸入您的問題（輸入 'q' 退出）：")
        if question.lower() == 'q':
            break

        embedding = vectorize_user_question(question)
        if embedding:
            query_qdrant(client, collection_name, embedding,top_k=5)
        else:
            print("問題向量化失敗，請重試！")

def main():
    """
    主程式入口
    """
    print("歡迎使用餐廳評論處理系統！")
    print("1. 清理評論")
    print("2. 生成嵌入向量")
    print("3. 上傳嵌入向量到 Qdrant")
    print("4. 查詢 Qdrant 資料庫")
    print("5. 退出")

    while True:
        choice = input("請選擇操作：")
        if choice == "1":
            clean_reviews()
        elif choice == "2":
            generate_embeddings()
        elif choice == "3":
            upload_to_qdrant()
        elif choice == "4":
            search_qdrant()
        elif choice == "5":
            print("再見！")
            break
        else:
            print("無效的選擇，請重新輸入！")

if __name__ == "__main__":
    main()
