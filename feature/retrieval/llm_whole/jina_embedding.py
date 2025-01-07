import requests
import json
import numpy as np

def embedding_jina(file_path, file_name):
    # API URL 和 Headers
    url = 'https://api.jina.ai/v1/embeddings'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer jina_6048b76532824efe82a449f8cd2b761bPvhOusuuPM-0GtWolcjrZb_XlvGx'
    }

    # 讀取檔案並處理內容
    file_path =  file_path # 檔案路徑
    with open(file_path, "r", encoding="utf-8") as file:
        text_content = file.read()

    # 將檔案內容切分為輸入句子列表
    inputs = text_content.split("。")  # 根據句號進行分割
    inputs = [sentence.strip() for sentence in inputs if sentence.strip()]  # 去掉空白行

    # API 請求數據
    data = {
        "model": "jina-embeddings-v3",
        "task": "text-matching",
        "late_chunking": False,
        "dimensions": 1024,
        "embedding_type": "float",
        "input": inputs
    }

    # 發送請求
    response = requests.post(url, headers=headers, json=data)

    # 驗證回應是否成功
    if response.status_code == 200:
        response_json = response.json()
        print(json.dumps(response_json, indent=4, ensure_ascii=False))
        
        # 提取嵌入向量
        embeddings = [item["embedding"] for item in response_json["data"]]
        
        # 確保嵌入數量和文本數量匹配
        if len(embeddings) != len(inputs):
            print("嵌入數量與輸入數量不匹配，請檢查輸入和回應！")
            exit()

        # 將嵌入向量轉為 NumPy 陣列並檢查形狀
        embeddings_array = np.array(embeddings)
        print(f"嵌入向量形狀: {embeddings_array.shape}")

        # 保存結果到 JSON 文件
        combined_data = [
            {
                "text": inputs[i],
                "vector": embeddings[i]
            }
            for i in range(len(inputs))
        ]

        with open(f"./embeding_data/{file_name}.json", "w", encoding="utf-8") as file:
            json.dump(combined_data, file, ensure_ascii=False, indent=4)

        print("嵌入向量和文本已成功保存到 combined_data.json")

    else:
        print(f"請求失敗，HTTP 狀態碼: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    embedding_jina(r"C:\Users\TMP214\Desktop\llm_1\cleaned_reviews\ChIJ______avQjQR2yhJGLY1Gto.txt", "ChIJ______avQjQR2yhJGLY1Gto.txt")