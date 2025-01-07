from langchain_openai import ChatOpenAI
from dotenv import dotenv_values

# 加載環境變量
config = dotenv_values("./.env")


# 初始化 OpenAI 模型
llm = ChatOpenAI(
    model="gpt-3.5-turbo",  # 可以改為 gpt-3.5-turbo 測試
    openai_api_key=config.get("chat_gpt_key")
)

def query_llm(prompt):
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"An error occurred: {e}"

# 測試用例
if __name__ == "__main__":
    print(query_llm("給我台北一日遊行程規劃"))