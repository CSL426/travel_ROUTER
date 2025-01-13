import mod.line as line
from mod import llm, embedding, csv_read, CBRA, type_check
from LLM import Cloud_fun
from LLM import store_fun

def main(user_Q: str):
    # user_Q = "請推薦我便宜的文青咖啡廳, 2024年12月26日下午3點, 台北車站" #匯入用戶需求
    # print(user_Q) #print出來用戶問題
    # one = line.line_user_input(user_Q) #輸出需求為變數one
    one = user_Q

    results = Cloud_fun(one)
    two = embedding.vector_search(results[0]) # 透過llm的「形容客戶行程的一句話」，用向量資料庫去對比搜尋
    three = csv_read.pandas_search(two, results[1]) # 透過向量資料庫跟llm的用戶特殊要求去抓出前100名符合的
    four = CBRA.CBRA(three, results[2]) # 透過結構搜尋跟庫基本要求資料再向下篩選出15個符合的

    result = store_fun(one)
    # 使用 best_three 函數篩選出最佳結果
    five = llm.best_three(four,result) #透過情境搜尋演算法篩出的15筆再用llm選出最佳的3筆資料
    # line.line_flex_message(five) #將llm挑選的最佳3筆帶入到line輸出的格式json來去輸出
    return five
