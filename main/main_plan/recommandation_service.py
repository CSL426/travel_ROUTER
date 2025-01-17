from feature.llm.LLM import LLM_Manager
from feature.retrieval.qdrant_search import qdrant_search  # 修改這裡
from feature.retrieval.utils import jina_embedding, json2txt, qdrant_control
from feature.plan import CBRA
from feature.sql import csv_read_2

def recommandation(user_Q, config):
    LLM_obj = LLM_Manager(config['ChatGPT_api_key']) # 初始化 LLM 物件

    one = user_Q
    results = LLM_obj.Cloud_fun(one)
    a = results[0] #LLM解析資料:形容客戶行程的一句話
    print(a)
    # b = results[1] #LLM解析資料:確認是否具有特殊要求
    b = [{'內用座位': False, '洗手間': False, '適合兒童': False, '適合團體': False, '現金': False, '其他支付': False, '收費停車': False, '免費停車': False, 'wi-fi': False, '無障礙': False}]
    c = results[2] #LLM解析資料:客戶基本要求資料
    print(c)
    qdrant_obj = qdrant_search(
        collection_name='view_restaurant_test',
        config=config,
        score_threshold=0,
        limit=100,
    )
    two = qdrant_obj.cloud_search(a) #透過llm的「形容客戶行程的一句話」，用向量資料庫去對比搜尋 
    three = csv_read_2.pandas_search(two, b) #透過向量資料庫跟llm的用戶特殊要求去抓出前100名符合的
    four = CBRA.run_test(three, c) #透過結構搜尋跟庫基本要求資料再向下篩選出15個符合的
    five = LLM_obj.store_fun(four) #透過情境搜尋演算法篩出的15筆再用llm選出最佳的3筆資料
    return five

if __name__ == "__main__":
    # 載入環境變數
    from dotenv import dotenv_values
    # 載入 .env 檔案中的環境變數
    config = dotenv_values("./.env")
    if len(config) == 0:
        print('please check .env path')


    five = recommandation("請推薦好吃台北餐廳", config)
    print(five)