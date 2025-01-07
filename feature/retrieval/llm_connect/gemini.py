from flask import Flask, request

import google.generativeai as genai
from dotenv import dotenv_values

# 網域設定
app = Flask(__name__) 

# LLM 設置
config = dotenv_values("./.env")
genai.configure(api_key=config.get("Gemini_API_KEY"))
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-latest",
)

# ------------------------------------------------
# API 設定

# URL/user_Q/<使用者問題> ; 返回 LLM 回答
@app.route("/user_Q/<user_Q>")
def question_anwser(user_Q):

    # 輸入問題給 gemini
    response = model.generate_content(
        str(user_Q),
    )

    print(response.text)
    return response.text



if __name__ == '__main__':
    # print(template_schedule())
    app.run(debug=True, host='0.0.0.0', port=5010)  