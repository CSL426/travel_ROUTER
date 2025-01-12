from feature.trip import TripPlanningSystem
from feature.sql import csv_read
from feature.retrieval import qdrant_search

# condition_dict = csv_read.load_and_sample_data('./database/info_df.csv')
# detail_info = [{'適合兒童': True, '無障礙': False, '內用座位': True}]

# result = csv_read.pandas_search(condition_data=condition_dict,
#                                 detail_info=detail_info)

from feature.retrieval.qdrant_search import qdrant_search
from dotenv import load_dotenv
import os

# 載入環境變數
load_dotenv()

# 設定配置
config = {
    'jina_url': os.getenv('JINA_URL'),
    'jina_headers_Authorization': os.getenv('JINA_AUTH'),
    'qdrant_url': os.getenv('QDRANT_URL'),
    'qdrant_api_key': os.getenv('QDRANT_API_KEY')
}

# 建立實例
qdrant_obj = qdrant_search(config=config)

# 使用方法
input_query = {'上午': '喜歡在文青咖啡廳裡享受幽靜且美麗的裝潢'}
result = qdrant_obj.trip_search(input_query)
