## 本地作業 : 
1. 向量化資料
2. 上傳雲端

* #### 單一文件流程 put_data2qdrant
1. text = 將文件格式化 json -> txt 以空白分割結合
2. `jina-embeding(` text `)`  : 向量化資料
3. 批量上傳 Qdrant 資料庫



## feature/retrival
1. 向量搜索資料庫端
- 使用方法 :

```
# 初始化物件
qdrant_obj = qdrant_search(collection_name, config) # config 要求請看物件說明文件


# 選擇方法
result = qdrant_obj.cloud_search(input_query)   # for 情境搜尋
result = qdrant_obj.trip_search(input_query)    # for 旅遊演算法

```
