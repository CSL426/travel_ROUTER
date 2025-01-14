from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict
from . import qdrant_search


class ParallelSearchManager:
    '''
    平行處理多時段搜尋的管理類別
    負責分配並整合多個時段的搜尋請求
    '''

    def __init__(self, config: dict):
        '''
        輸入:
            config: dict
                必要的設定參數，包含:
                - jina_url
                - jina_headers_Authorization
                - qdrant_url
                - qdrant_api_key
        '''
        self.qdrant_obj = qdrant_search(
            collection_name='view_restaurant_test',
            config=config,
            score_threshold=0,
            limit=50,
        )

    def parallel_trip_search(self, input_queries: List[Dict]) -> Dict:
        '''
        平行處理多個時段的向量搜尋

        輸入:
            input_queries: List[Dict] 多個時段的搜尋需求
            格式: [
                {'上午': '文青咖啡廳描述'}, 
                {'中餐': '餐廳描述'}
                ...
            ]

        輸出:
            Dict: 合併後的搜尋結果
            格式: {
                '上午': ['place_id1', 'place_id2'...],
                '中餐': ['place_id3', 'place_id4'...],
                ...
            }
        '''
        def search_single_query(query: Dict) -> Dict:
            '''處理單一時段的搜尋'''
            return self.qdrant_obj.trip_search(query)

        # 使用 ThreadPoolExecutor 進行平行處理
        results = {}
        with ThreadPoolExecutor() as executor:
            # 提交所有搜尋任務
            future_to_query = {
                executor.submit(search_single_query, query): query
                for query in input_queries
            }

            # 收集所有結果
            for future in future_to_query:
                try:
                    result = future.result()
                    results.update(result)
                except Exception as e:
                    print(f"搜尋過程發生錯誤: {str(e)}")
                    continue

        return results


# 測試用程式碼
if __name__ == "__main__":
    # 測試設定
    config = {
        'jina_url': 'your_jina_url',
        'jina_headers_Authorization': 'your_auth',
        'qdrant_url': 'your_qdrant_url',
        'qdrant_api_key': 'your_api_key'
    }

    # 測試資料
    input_queries = [
        {'上午': '喜歡在文青咖啡廳裡享受幽靜且美麗的裝潢'},
        {'中餐': '好吃很辣便宜加飯附湯環境整潔很多人可以停車'}
    ]

    # 執行測試
    searcher = ParallelSearchManager(config)
    result = searcher.parallel_trip_search(input_queries)
    print(result)
