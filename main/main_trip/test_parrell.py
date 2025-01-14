# test.py

from dotenv import load_dotenv
import os
from feature.retrieval.qdrant_search import qdrant_search
import time
from concurrent.futures import ThreadPoolExecutor


def test_search():
    """測試平行搜尋功能"""
    # 載入環境變數
    load_dotenv()

    # 準備測試資料
    test_queries = [
        {'上午': '喜歡在文青咖啡廳裡享受幽靜且美麗的裝潢'},
        {'中餐': '好吃很辣便宜加飯附湯環境整潔很多人可以停車'},
        {'下午': '充滿歷史感的日式建築'},
        {'晚餐': '適合多人聚餐的餐廳'},
        {'晚上': '可以看夜景的地方'}
    ]
    print(len(test_queries))

    try:
        # 建立 qdrant_search 實例
        config = {
            'jina_url': os.getenv('jina_url'),
            'jina_headers_Authorization': os.getenv('jina_headers_Authorization'),
            'qdrant_url': os.getenv('qdrant_url'),
            'qdrant_api_key': os.getenv('qdrant_api_key')
        }

        qdrant_obj = qdrant_search(
            collection_name='view_restaurant_test',
            config=config
        )

        # 記錄開始時間
        start_time = time.time()

        # 直接搜尋版本
        print("\n=== 開始單一搜尋測試 ===")
        single_results = {}
        for query in test_queries:
            result = qdrant_obj.trip_search(query)
            single_results.update(result)
        single_time = time.time() - start_time

        # 重置開始時間
        start_time = time.time()

        # 平行處理版本
        print("\n=== 開始平行搜尋測試 ===")
        parallel_results = {}
        with ThreadPoolExecutor() as executor:
            future_to_query = {
                executor.submit(qdrant_obj.trip_search, query): query
                for query in test_queries
            }
            for future in future_to_query:
                try:
                    result = future.result()
                    parallel_results.update(result)
                except Exception as e:
                    print(f"搜尋發生錯誤: {str(e)}")
        parallel_time = time.time() - start_time

        # 輸出結果與時間比較
        print("\n=== 執行時間比較 ===")
        print(f"單一搜尋執行時間: {single_time:.2f} 秒")
        print(f"平行搜尋執行時間: {parallel_time:.2f} 秒")
        print(f"時間差異: {single_time - parallel_time:.2f} 秒")

        # 輸出一些結果範例
        print("\n=== 搜尋結果範例 ===")
        for period, ids in single_results.items():
            print(f"\n{period}:")
            print(f"找到 {len(ids)} 個地點")
            print("前3個ID:", ids[:3] if ids else "無結果")

    except Exception as e:
        print(f"測試過程發生錯誤: {str(e)}")


if __name__ == "__main__":
    test_search()
