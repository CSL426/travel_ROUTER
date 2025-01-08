import mod.line as line
from mod import llm, embedding, csv_read, CBRA, type_check

def main(user_Q : str):
    # user_Q = "請推薦我便宜的文青咖啡廳, 2024年12月26日下午3點, 台北車站" #匯入用戶需求
    # print(user_Q) #print出來用戶問題
    # one = line.line_user_input(user_Q) #輸出需求為變數one
    one = user_Q
    a = llm.sentence_for_embedding(one) #LLM解析資料:形容客戶行程的一句話
    b = llm.detail_info(one) #LLM解析資料:確認是否具有特殊要求
    c = llm.require_info(one) #LLM解析資料:客戶基本要求資料
    two = embedding.vector_search(a) #透過llm的「形容客戶行程的一句話」，用向量資料庫去對比搜尋
    three = csv_read.pandas_search(two, b) #透過向量資料庫跟llm的用戶特殊要求去抓出前100名符合的
    four = CBRA.CBRA(three, c) #透過結構搜尋跟庫基本要求資料再向下篩選出15個符合的
    five = llm.best_three(four) #透過情境搜尋演算法篩出的15筆再用llm選出最佳的3筆資料
    # line.line_flex_message(five) #將llm挑選的最佳3筆帶入到line輸出的格式json來去輸出
    return five