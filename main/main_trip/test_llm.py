import os
from dotenv import load_dotenv
from feature.llm.LLM import LLM_Manager

load_dotenv()
ChatGPT_api_key = os.getenv('ChatGPT_api_key')

LLM_obj = LLM_Manager(ChatGPT_api_key)

user_input = "文青咖啡廳 1/14上午9點出發晚上8點回家"
a, b, c = LLM_obj.Thinking_fun(user_input)

print(a)
print(b)
print(c)

