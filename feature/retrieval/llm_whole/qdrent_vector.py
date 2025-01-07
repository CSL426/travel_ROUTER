import os
import json
from qdrant_client import QdrantClient
from llm_whole.search_filepath import total_file_path
from llm_whole.search_by_cos import list_placeids

# from qdrant_client import QdrantClient
collection_name="example_collection"
qdrant_client = QdrantClient(
    url="https://7ea5deab-8a79-4c4f-bbc3-edb3f5f98a03.us-east4-0.gcp.cloud.qdrant.io:6333", 
    api_key="jPdSAiS9gE7xrk-gLA8NPqPkigvhr2uHfx1tQmdfGsV0eB3l2bP72A",
)
# from qdrant_client import QdrantClient
# print(qdrant_client.get_collections())

# 确保集合存在
if not qdrant_client.collection_exists("example_collection"):
    qdrant_client.create_collection(
        collection_name="example_collection",
        vectors_config={"size": 1024, "distance": "Cosine"}  # 设置向量维度和距离度量方式
    )
    print(f"集合 example_collection 已创建")
else:
    print(f"集合 example_collection 已存在")

# 文件夹路径
folder_path = "./embeding_data"

# 遍历文件夹中的所有 JSON 文件
for file_name in os.listdir(folder_path):
    if file_name.replace(".json", "") in list_placeids(qdrant_client, collection_name) :  # 我的資料在 collection 中時我不上傳
        print("資料已有, 不上傳")
        continue
    else :
        file_path = f"C:/Users/TMP214/Desktop/llm_1/cleaned_reviews/{file_name}.txt"  # 檔案路徑
        print(file_path)
        if file_name.endswith(".json"):  # 确保只处理 .json 文件
            file_path = os.path.join(folder_path, file_name)
            print(f"正在处理文件: {file_name}")

            # 去掉文件扩展名 `.json`，作为 payload 的值
            clean_name = os.path.splitext(file_name)[0]

            # 读取 JSON 文件内容
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            # 提取向量
            vectors = [item["vector"] for item in data]

            # 替换 payload 为文件名（去掉 .json 的部分）
            # payload = [{"file_name": clean_name} for _ in data]
            # payload = [item["text"] for item in data]
            payload = [{"file_name": clean_name, "text": item["text"]} for item in data]

            # 上传数据到 Qdrant 集合
            qdrant_client.upload_collection(
                collection_name=collection_name,
                vectors=vectors,
                payload=payload
            )
            print(f"已上传文件: {file_name}")

print("所有文件已处理完成！")


# import os
# import json
# from qdrant_client import QdrantClient
# from llm_whole.search_filepath import total_file_path  # 假設 `total_file_path` 是自定義的函數

# # 初始化 Qdrant 客户端
# qdrant_client = QdrantClient(
#     url="https://7ea5deab-8a79-4c4f-bbc3-edb3f5f98a03.us-east4-0.gcp.cloud.qdrant.io:6333", 
#     api_key="jPdSAiS9gE7xrk-gLA8NPqPkigvhr2uHfx1tQmdfGsV0eB3l2bP72A",
# )

# # 确保集合存在
# if not qdrant_client.collection_exists("example_collection"):
#     qdrant_client.create_collection(
#         collection_name="example_collection",
#         vectors_config={"size": 1024, "distance": "Cosine"}  # 设置向量维度和距离度量方式
#     )
#     print(f"集合 example_collection 已创建")
# else:
#     print(f"集合 example_collection 已存在")

# # 文件夾路徑
# embedding_folder = "./embedding_data"  # 嵌入向量資料夾
# review_folder = r".\餐廳評論爬蟲 (1)"  # 原始評論資料夾
# cleaned_folder = r".\cleaned_reviews"  # 清理後的評論資料夾

# # 遍历餐廳評論檔案
# for name in total_file_path(review_folder)[:10]:
#     # 確保名稱一致
#     name_without_ext = os.path.splitext(name)[0]

#     # 檢查是否已嵌入
#     if f"{name_without_ext}.json" in total_file_path(embedding_folder):
#         print(f"資料已存在，跳過: {name}")
#         continue
#     else:
#         # 建立嵌入檔案路徑
#         file_path = os.path.join(cleaned_folder, f"{name_without_ext}.txt")
#         if not os.path.exists(file_path):
#             print(f"清理後的檔案不存在，跳過: {name}")
#             continue

#         print(f"正在處理檔案: {file_path}")

#         # 讀取清理後的評論文本
#         with open(file_path, "r", encoding="utf-8") as f:
#             text_data = f.read()

#         # 假設你已經有一個函數生成向量（例如 embedding_jina）
#         embedding = [[0.1] * 1024]  # 模擬生成的向量
#         print(f"嵌入向量形狀: {len(embedding)} x {len(embedding[0])}")

#         # 保存嵌入向量到 JSON 文件
#         output_path = os.path.join(embedding_folder, f"{name_without_ext}.json")
#         with open(output_path, "w", encoding="utf-8") as file:
#             json.dump([{"vector": embedding[0], "text": text_data}], file, ensure_ascii=False, indent=4)
#         print(f"嵌入向量已保存: {output_path}")

#         # 提取向量和 payload
#         vectors = [embedding[0]]
#         payload = [{"file_name": name_without_ext, "text": text_data}]

#         # 上傳到 Qdrant
#         qdrant_client.upload_collection(
#             collection_name="example_collection",
#             vectors=vectors,
#             payload=payload
#         )
#         print(f"已上传文件到 Qdrant: {name_without_ext}.json")

# print("所有文件已處理完成！")
