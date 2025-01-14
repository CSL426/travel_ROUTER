from feature.retrieval.qdrant_search import qdrant_search
from dotenv import load_dotenv
import os

try:
    # 載入 .env
    load_dotenv()

    # 使用環境變數
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
    input_query = {'上午': '喜歡在文青咖啡廳裡享受幽靜且美麗的裝潢'}
    input_query = {'中餐': '好吃很辣便宜加飯附湯環境整潔很多人可以停車'}
    result = qdrant_obj.trip_search(input_query)
    print(result)
except Exception as e:
    print(f"錯誤：{str(e)}")
