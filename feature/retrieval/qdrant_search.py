from qdrant_client import QdrantClient, models
from dotenv import dotenv_values

from .utils.jina_embedding import jina_embedding
from .utils.qdrant_control import qdrant_manager

class qdrant_search:
    '''
    #### 向量搜尋端 :
    ---
    - input :  

        ```
        config = {
                    'jina_url':str, 
                    'jina_headers_Authorization':str,
                    'qdrant_url': str,
                    'qdrant_api_key': str
                }
        ```
    
    - 

    ---
    - 流程 :
        1. vector = 將 ["形容客戶行程的一句話"] 直接向量化
        2. 使用 vector 搜尋 qdrant 回傳 '相似度 > 某個分數' 的資料

    ---
    - method :

        ```
        .cloud_search( input_query: list[str] = ["形容客戶行程的一句話"] )
        .trip_search( input_query: dict[list])
        ```
    '''
    def __init__(
        self,
        config: dict = {
                'jina_url':str, 
                'jina_headers_Authorization':str,
                'qdrant_url': str,
                'qdrant_api_key': str
            }
        ):
        
        self.config = config


    def __search_query(self, input_query):
        '''
        - 主函數，負責搜尋
        - output :  

            ```
            return [{
                        "Place ID 1":{"分數":"int"} ,      # 相似分數 
                        "Place ID 2":{"分數":"int"} , 
                        …, 
                        "Place ID n":{"分數":"int"} 
                    }]
            ```
        '''
        config = self.config

         # 1. 將 ["形容客戶行程的一句話"] 直接向量化
        embedding_data = jina_embedding(input_query, '', config['jina_url'], config['jina_headers_Authorization'])
        vector = embedding_data['embedding']   # dim = 1024

        # 2. 使用 vector 搜尋 qdrant 回傳 '相似度 > 某個分數' 的資料
        qdrant_obj = qdrant_manager(collection_name='test1', 
                                    qdrant_url=config.get("qdrant_url"),
                                    qdrant_api_key= config.get("qdrant_api_key"))
        result = qdrant_obj.search_vector(vector, 0.5)
        return result


    def cloud_search(self, input_query: list[str])-> list[dict]:
        '''
        - input :

            ```
            input_query: list[str] = ["形容客戶行程的一句話"]
            ```
        - output :

            ```
            return [{
                "Place ID 1":{"分數":"int"} ,      # 相似分數 
                "Place ID 2":{"分數":"int"} , 
                …, 
                "Place ID n":{"分數":"int"} 
            }]
            ```
        '''
        result = self.__search_query(input_query)
        return result
    
    def trip_search(self, input_query: dict)-> dict[list]: 
        '''
        - input :

            ```
            input_query: dict = { "上午" : "形容客戶行程的一句話"}
            ```
        output :

            ```
            return { period : ["PlaceID", "PlaceID", …, "PlaceID"]} 
            ```
        '''
        period, text = next(iter(input_query.items()))
        result = list(self.__search_query(text)[0].keys())

        return {period : result}


if __name__ == "__main__":
    # 加載環境變量
    config = dotenv_values("./.env")
    if len(config) == 0:
        print('please check .env path')

    qdrant_obj = qdrant_search(config)

    # 情境搜索
    input_query = ['喜歡在文青咖啡廳裡享受幽靜且美麗的裝潢']
    input_query = ['''
        這家餐廳的氛圍溫暖宜人，精湛的烤功與復古風格交織，讓人一踏進來就感受到無比的舒適感。
        進入這家餐廳，溫馨的環境搭配精緻的烤肉技術，營造出一種獨特的復古氛圍。
        這家餐廳不僅提供美味的烤肉，還以其溫馨的裝潢和復古風格打破了傳統餐飲的格局。
        這裡有著溫暖的氛圍，烤肉技術一流，並且每個細節都透露出復古的魅力。
        餐廳內部充滿溫暖的氣息，烤製的美食口感十足，復古的風格設計也讓人如沐春風。
        這家餐廳的設計讓人感到溫馨舒適，精湛的烤肉技術搭配上迷人的復古風格，為每位顧客帶來獨特的用餐體驗。
        溫馨的餐廳氛圍搭配烤肉的香氣，復古風格的裝潢讓這家餐廳成為別具一格的美食天堂。
        在這間餐廳中，您將感受到濃厚的溫暖氛圍，品嚐到極具特色的烤肉，並享受復古風格所帶來的懷舊感。
        這是一家溫馨又充滿情調的餐廳，精緻的烤肉和復古風格的設計，營造出難以忘懷的用餐體驗。
        這家餐廳給人一種親切的感覺，烤肉技術一流，復古的裝潢讓您回味無窮。
                   ''']
    result = qdrant_obj.cloud_search(input_query)
    
    # 旅遊搜索
    input_query = {'上午': '喜歡在文青咖啡廳裡享受幽靜且美麗的裝潢'}
    # result = qdrant_obj.trip_search(input_query)

    print(result)