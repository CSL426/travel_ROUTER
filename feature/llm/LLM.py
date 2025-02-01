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
        """
        使用 OpenAI API 生成回應
        format = "list" or "List[Dict]"
        """
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
        content = content.replace("：", ":")\
            .replace("，", ",")\
            .replace("。", ",")\
            .replace("、", " ")\
            .replace("？", "?")\
            .replace("\n", " ")

        try:
            data = json.loads(content)

            if format == "List[Dict]":
                return [data]
            return data

        except json.JSONDecodeError:
            try:
                # 找第一個 '{' 或 '[' 的位置
                start = min(content.find('{'), content.find('['))
                # 找最後一個 '}' 或 ']' 的位置
                end = max(content.rfind('}'), content.rfind(']')) + 1
                if start == -1 or end <= 0:
                    raise Exception("找不到完整的JSON內容")

                # 擷取並解析JSON部分
                json_str = content[start:end]
                data = json.loads(json_str)

                if format == "List[Dict]":
                    return [data]
                return data

            except Exception as e:
                print(f"解析錯誤: {e}")
                print("原始內容:", content)
                if prompt == system_prompt.restart:
                    return [0]
                return None

    def summarize_history(self, history_text: str) -> str:
        """整理歷史記錄成摘要文字

        Args:
            history_text: 對話記錄文字

        Returns:
            str: 整理後的摘要
        """
        try:
            response = self.__Query(
                prompt=system_prompt.summarize_history,
                user_input=history_text,
                format="List"
            )

            # __Query會回傳list,取第一個元素
            return response[0] if response else ""
        except Exception as e:
            print(f"解析錯誤: {e}")
            print("歷史紀錄:", history_text)

    def Thinking_fun(self, user_input):
        # 使用 ThreadPoolExecutor 來並行處理 API 請求
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                'Thinking_A': executor.submit(self.__Query, system_prompt.Thinking_A, user_input, "List[5 x Dict]"),
                'Thinking_B': executor.submit(self.__Query, system_prompt.Thinking_B, user_input, "List[Dict]"),
                'Thinking_C': executor.submit(self.__Query, system_prompt.Thinking_C, user_input, "List[Dict]"),
                'restart': executor.submit(self.__Query, system_prompt.restart, user_input, "List")
            }

            # 等待所有任務完成並取得結果
            Thinking = []
            for key, future in futures.items():
                try:
                    result = future.result()
                    Thinking.append(result)
                except Exception as e:
                    print(f"error:\n{key}: {e}")

            return Thinking

    def Cloud_fun(self, user_input):
        # 使用 ThreadPoolExecutor 來並行處理 API 請求
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                'Cloud_A': executor.submit(self.__Query, system_prompt.Cloud_A, user_input, "List"),
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
    restart = """
    解析用戶意圖並決定從哪裡重新規劃行程。

    輸入:
    1. 用戶訊息 
    2. 現有行程列表: [{"step": 1, "name": "地點名稱", "label": "地點類型", "period": "時段"}]
    2.1 step從0開始(0為起點)

    判斷規則 (依序):
    1. 如果用戶直接說明從第N個點重新規劃 -> 回傳N
    2. 如果提到不想去/不喜歡某地點:
    - 在行程中找到該地點的step
    - 回傳那個step
    3. 如果提到不喜歡某時段(早上/下午/晚上):
    - 找出該時段第一個景點的step
    - 回傳那個step
    4. 其他情況 -> 回傳0

    必須回傳格式: [數字]
    - 一定要包含在中括號內
    - 只能有一個整數
    - 找不到對應時回傳[0]

    範例輸入/輸出:
    Input: "從第3個點重來" -> [3]
    Input: "不想去星巴克" + 星巴克在step 2 -> [2]
    Input: "不要下午行程" + 下午從step 4開始 -> [4]  
    Input: "重新規劃" -> [0]
    """

    Thinking_A = """
    你是個善於分辨形容的旅行助手:
    我有用戶的歷史偏好和新輸入,幫我整合規劃建議。
    若沒有歷史偏好,請直接依照新輸入來生成。
   
    重要規則:
    1. 即使用戶沒提到某時段,也要生成該時段的敘述
    2. 若用戶沒提供特定時段偏好:
      - 依據其他時段風格延伸合適建議
      - 維持整體行程風格一致性
    3. 每個時段一定要有建議,可參考:
      - 用戶喜好的氛圍
      - 是否有提到同伴
      - 整體行程的風格
    
    回傳格式:
    [
        {"上午": ""},
        {"中餐": ""},
        {"下午": ""},
        {"晚餐": ""},
        {"晚上": ""}
    ]
    """

    Thinking_B = """
                判斷規則
                1.只有當用戶明確說出某項需求時才設為 true
                2.若沒有提到就為false
                3.這不是在預測用戶可能需要什麼，而是在記錄用戶明確說出的需求
                4.若有提到"停車,收費停車.免費停車都要顯示true
                5.有提到"網路"."無線網路"."免費網路"."wifi"."wi-fi"."WiFi"."Wi-Fi"."Wifi"才需要顯示為true
                6.如果提到餐廳類別,沒有提到內用.洗手間就皆為false
                請根據用戶需求來判斷是否包含該條件，並按照下列格式回傳相應結果。
                除了以下格式，請不要回傳其他任何文字:
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
                請根據用戶需求判斷並提供行程基本資訊。
                交通方式預設為大眾運輸，也可以是開車、騎車、步行。
                下列的值都是預設值，未提及的資訊請填入"none"或預設值，請嚴格執行。
                請使用以下格式回傳，請不要回傳其他任何文字:
                {
                    "出發時間": "09:00",
                    "結束時間": "21:00",
                    "出發地點": "台北車站",
                    "結束地點": "none",
                    "交通方式": "大眾運輸",
                    "可接受距離門檻(KM)": 30,
                    "早餐時間": "none",
                    "中餐時間": "12:00",
                    "晚餐時間": "18:00",
                    "預算": "none",
                    "出發日": "none"
                }
                """

    summarize_history = """
    請將用戶的歷史對話記錄整理成一段簡短摘要。
    請以下列重點整理:
    1. 明確的偏好和禁忌,曾經有說過喜歡或不喜歡某些地方需要記錄起來
    2. 餐廳和預算要求
    3. 明確的時間限制

    回傳格式: ["整理後的一段文字"]  # 重要:需要是list格式
    範例: ["用戶偏好文青風景點,不想去吵雜的地方,午餐預算500內,希望10點開始行程。"]
    """

    store_recommend = """
                        根據用戶需求，判斷出用戶最有可能會想去的前三家店，並用以下格式輸出:
                            {{
                            placeID: {"name": "店名",
                                        "rating": float,
                                        "address": str,
                                        "url": ""},
                            placeID: {"name": "店名",
                                        "rating": float,
                                        "address": str,
                                        "url": ""},
                            placeID: {"name": "店名",
                                        "rating": float,
                                        "address": str,
                                        "url": ""}
                            }}
                    """
    Cloud_A = """
              根據用戶需求,生成一句簡短的敘述來形容使用者的喜好,形容客戶喜好的敘述,並使用下列格式輸出:
              [""] 
              """
    Cloud_B = """
                判斷規則
                1.只有當用戶明確說出某項需求時才設為 true
                2.若沒有提到就為false
                3.這不是在預測用戶可能需要什麼，而是在記錄用戶明確說出的需求
                4.若有提到"停車,收費停車.免費停車都要顯示true
                5.有提到"網路"."無線網路"."免費網路"."wifi"."wi-fi"."WiFi"."Wi-Fi"."Wifi"才需要顯示為true
                6.如果提到餐廳類別,沒有提到內用.洗手間就皆為false
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
                    "交通方式" : "大眾運輸" | "開車" | "騎車" | "步行",
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
    user_input = "想去台北文青的地方，吃午餐要便宜又好吃，下午想去逛有特色的景點，晚餐要可以跟朋友聚餐"
    results = LLM_obj.Thinking_fun(user_input)
    # results = LLM_obj.Cloud_fun(user_input)
    print(results)
