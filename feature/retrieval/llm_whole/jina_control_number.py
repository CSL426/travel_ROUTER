from llm_whole.search_filepath import total_file_path
from llm_whole.jina_embedding import embedding_jina


# 讀取檔案並處理內容
for name in total_file_path(r".\餐廳評論爬蟲 (1)")[0:10]:
    if name in total_file_path('embeding_data') :  # 我的資料在 file path 中時我不 embbeding
        print("資料已有, 不向量")
        continue
    else :
        file_path = f"C:/Users/TMP214/Desktop/llm_1/cleaned_reviews/{name}.txt"  # 檔案路徑
        print(file_path)

        embedding_jina(file_path, name)
    # with open(file_path, "r", encoding="utf-8") as file:
    #     text_content = file.read()
