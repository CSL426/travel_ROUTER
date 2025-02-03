import openai
import json
from dotenv import load_dotenv
import os
import concurrent.futures  # 引入並行處理模組

from feature.llm.utils import system_prompt

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


if __name__ == "__main__":
    from pprint import pprint
    # 從環境變量中讀取 OpenAI API 金鑰
    load_dotenv()
    ChatGPT_api_key = os.getenv('ChatGPT_api_key')

    # 初始化物件
    LLM_obj = LLM_Manager(ChatGPT_api_key)

    # 呼叫 Thinking 和 Cloud 的並行處理函數
    user_input = "想去台北文青的地方，吃午餐要便宜又好吃，下午想去逛有特色的景點，晚餐要可以跟朋友聚餐"
    
    
    # ====================================================
    results = LLM_obj.Thinking_fun(user_input)
    print('======旅遊推薦======')
    print(f'input query = {user_input}\n')
    pprint(results, sort_dicts=False)
    print('\n\n')

    # ====================================================
    results = LLM_obj.Cloud_fun(user_input)
    print('======情境搜索======')
    print(f'input query = {user_input}\n')
    pprint(results, sort_dicts=False)
    
