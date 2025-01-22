import ast
import openai
import json
from dotenv import load_dotenv
import os
import concurrent.futures  # 引入並行處理模組


class LLM_Manager:
    def __init__(self, ChatGPT_api_key):
        openai.api_key = ChatGPT_api_key  # 使用 ChatGPT_api_key 來設定 OpenAI API 金鑰

    def __Query(self, prompt, user_input, format):
        '''
        使用 OpenAI API 生成回應
        format = "list" or "List[Dict]"
        '''
        # 檢查類型檢查和轉換,使用 json.dumps 轉換為字符串
        if isinstance(user_input, (list, dict)):
            user_input = json.dumps(user_input, ensure_ascii=False)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=800
        )
        content = response['choices'][0]['message']['content'].strip()
        # 根據format不同進行處理
        if format == "list":
            return json.loads(content)
        elif format == "List[Dict]":
            return [json.loads(content)]  # 返回字典列表格式
        elif format == "List[5 x Dict]":
            return json.loads(content)

    def Thinking_fun(self, user_input):
        # 使用 ThreadPoolExecutor 來並行處理 API 請求
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                'Thinking_A': executor.submit(self.__Query, system_prompt.Thinking_A, user_input, "List[5 x Dict]"),
                'Thinking_B': executor.submit(self.__Query, system_prompt.Thinking_B, user_input, "List[Dict]"),
                'Thinking_C': executor.submit(self.__Query, system_prompt.Thinking_C, user_input, "List[Dict]"),
                'restart':executor.submit(self.__Query, system_prompt.restart, user_input, "List")
            }

            # 等待所有任務完成並取得結果
            Thinking = []
            for key, future in futures.items():
                result = future.result()
                Thinking.append(result)

            return Thinking

    def Cloud_fun(self, user_input):
        # 使用 ThreadPoolExecutor 來並行處理 API 請求
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                'Cloud_A': executor.submit(self.__Query, system_prompt.Cloud_A, user_input, "list"),
                'Cloud_B': executor.submit(self.__Query, system_prompt.Cloud_B, user_input, "List[Dict]"),
                'Cloud_C': executor.submit(self.__Query, system_prompt.Cloud_C, user_input, "List[Dict]")
            }

            # 等待所有任務完成並取得結果
            Cloud = []
            for _, future in futures.items():
                result = future.result()
                Cloud.append(result)

            return Cloud

    def store_fun(self, user_input):
        result = self.__Query(system_prompt.store_recommend,
                              user_input, "List[Dict]")
        Store = result
        return Store


class system_prompt:
    restart='''
            我有上一次的行程輸入與用戶輸入，幫我判斷用戶想要完全重新開始或是從哪個點開始重新規劃:
            restart_index = 0: 完全重新規劃
            restart_index = N: 從第N個點開始重新規劃,即第N個點後重新安排
            '''
    Thinking_A = '''
                你是個善於分辨形容的旅行助手:
                我有上一次的行程輸入、用戶需求與用戶輸入，幫我整合成新的建議，
                若沒有上一次的行程輸入、用戶需求，請直接依照用戶輸入來生成，
                請生成行程建議，請按照以下格式回應。
                [
                    {"上午": ""}, 
                    {"中餐": ""}, 
                    {"下午": ""}, 
                    {"晚餐": ""}, 
                    {"晚上": ""} 
                ]
                '''
    Thinking_B = """
                請根據用戶需求來判斷是否包含該條件，並按照下列格式回傳相應結果：
                {
                    "內用座位": true|false,
                    "洗手間": true|false,
                    "適合兒童": true|false,
                    "適合團體": true|false,
                    "現金": true|false,
                    "其他支付": true|false,
                    "收費停車": true|false,
                    "免費停車": true|false,
                    "wi-fi": true|false,
                    "無障礙": true|false
                }
                """
    # Thinking_C "結束時間"判定會出問題,還需要修正
    Thinking_C = """
                我有上一次的行程輸入、用戶需求與用戶輸入，幫我整合成新的建議，
                若沒有上一次的行程輸入、用戶需求，請直接依照用戶輸入來生成，
                請根據用戶需求來判斷並提供以下行程規劃資訊，如果沒有提到某個需求，請設為 "none",並按照下列格式回傳相應結果：
                {
                    "出發時間": "00:00" | "none",
                    "結束時間": "00:00" | "none",
                    "出發地點": str | "none",
                    "結束地點": str | "none",
                    "交通方式": "大眾運輸" | "開車" | "騎自行車" | "步行",
                    "可接受距離門檻(KM)": int | "none",
                    "早餐時間": "00:00" | "none",
                    "中餐時間": "00:00" | "none",
                    "晚餐時間": "00:00" | "none",
                    "預算": int | "none",
                    "出發日": "mm-dd" | "none"
                }
                """
    store_recommend = """
                        根據用戶需求，判斷出用戶最有可能會想去的前三家店，並用以下格式輸出:
                            {{
                            placeID : { "name" : "店名",
                                        "rating" : float,
                                        "address": str, 
                                        "url" : ""} ,
                            placeID : { "name" : "店名",
                                        "rating" : float,
                                        "address": str, 
                                        "url" : ""} ,
                            placeID : { "name" : "店名",
                                        "rating" : float,
                                        "address": str, 
                                        "url" : ""}
                            }}
                    """
    Cloud_A = """
              根據用戶需求,生成一句簡短的敘述來形容使用者的喜好,形容客戶喜好的敘述,並使用下列格式輸出:
              [""] 
              """
    Cloud_B = """
                請根據用戶需求來判斷是否包含該條件，並按照下列格式回傳相應結果：
                {{
                    "內用座位": true|false,
                    "洗手間": true|false,
                    "適合兒童": true|false,
                    "適合團體": true|false,
                    "現金": true|false,
                    "其他支付": true|false,
                    "收費停車": true|false,
                    "免費停車": true|false,
                    "wi-fi": true|false,
                    "無障礙": true|false
                }}
                """
    Cloud_C = """
                請根據用戶需求來判斷並提供以下行程規劃資訊，如果沒有提到某個需求，請設為 "none",並按照下列格式回傳相應結果：
                {{
                    "星期別": int | "none",
                    "時間": "hh:mm" | "none",
                    "類別":  餐廳 | 咖啡廳 | 小吃 | 景點,
                    "預算": int | "none",
                    "出發地點": str | "none",
                    "可接受距離門檻(KM)" : int | “none”,
                    "交通方式" : "大眾運輸" | "開車" | "騎自行車" | "步行",
                }}
                """

if __name__ == "__main__":
    # 從環境變量中讀取 OpenAI API 金鑰
    load_dotenv()
    ChatGPT_api_key = os.getenv('ChatGPT_api_key')

    # 初始化物件
    LLM_obj = LLM_Manager(ChatGPT_api_key)

    # 呼叫 Thinking 和 Cloud 的並行處理函數
    user_input = "文青咖啡廳"
    results = LLM_obj.Thinking_fun(user_input)
    # results = LLM_obj.Cloud_fun(user_input)
    print(results)
