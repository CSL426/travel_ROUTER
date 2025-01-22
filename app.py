from dotenv import dotenv_values
from flask import Flask, request, abort
from linebot import LineBotApi
from linebot.webhook import WebhookHandler
from linebot.exceptions import InvalidSignatureError  # 確保這是從新版 SDK 來的
from linebot.models import MessageEvent, TextMessage, FlexSendMessage
from linebot.models import FlexSendMessage, CarouselContainer

from feature.line.bubbles_seting.First_bubble import First
from feature.line.bubbles_seting.Second_bubble import Second
from feature.line.bubbles_seting.Third_bubble import Third
from feature.line.Vibe import thinking  # 載入 Vibe 函數

from main.main_trip import run_trip_planner
from main.main_plan.recommandation_service import recommandation

# 載入 .env 檔案中的環境變數
config = dotenv_values("./.env")
if len(config) == 0:
    print('please check .env path')

# 讀取 LINE 的環境變數
LINE_CHANNEL_ACCESS_TOKEN = config["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = config["LINE_CHANNEL_SECRET"]


# 初始化 Flask 應用
app = Flask(__name__)

# 初始化 LineBotApi 和 WebhookHandler
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 設定 /callback 路由，處理 LINE webhook 請求
@app.route("/callback", methods=['POST'])
def callback():
    app.logger.info("Received webhook request")
    app.logger.info(f"Headers: {request.headers}")
    app.logger.info(f"Body: {request.get_data(as_text=True)}")
    # 取得 X-Line-Signature 標頭值
    signature = request.headers['X-Line-Signature']

    # 取得請求的 body 內容
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # 簽名驗證
    try:
        handler.handle(body, signature)  # 使用 handler 來處理簽名驗證
    except InvalidSignatureError:
        app.logger.error("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)  # 若簽名無效，返回 400 錯誤碼

    return 'OK'

# 處理消息事件
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text_message = event.message.text

    user_Q = text_message[5:]
    text_message = text_message[0:4]
    
    if text_message == "旅遊推薦":
        # 預設的旅遊推薦資料
        '''
        data = [
            {
                "name": "家",
                "start_time": "08:00",
                "end_time": "08:30",
                "duration": 30,
                "hours": "08:00-08:30",
                "transport": {
                    "mode": "步行",
                    "time": 0,
                    "period": "00:00-00:00"
                }
            },
            {
                "name": "台北101",
                "start_time": "09:00",
                "end_time": "11:30",
                "duration": 150,
                "hours": "09:00-11:30",
                "transport": {
                    "mode": "大眾運輸",
                    "time": 15,
                    "period": "08:45-09:00"
                }
            },
            {
                "name": "鼎泰豐(信義店)",
                "start_time": "11:32",
                "end_time": "13:02",
                "duration": 90,
                "hours": "11:32-13:02",
                "transport": {
                    "mode": "步行",
                    "time": 5,
                    "period": "11:25-11:30"
                }
            },
            {
                "name": "信義威秀商圈",
                "start_time": "13:08",
                "end_time": "14:08",
                "duration": 60,
                "hours": "13:08-14:08",
                "transport": {
                    "mode": "開車",
                    "time": 10,
                    "period": "13:00-13:10"
                }
            }
        ]
        '''

        data = run_trip_planner(user_Q)
        # 創建 carousel 的內容
        A1 = {
            "type": "carousel",
            "contents": [
                First(data),  # 呼叫 First_bubble 函數來生成第一個 Bubble
                Second(data),  # 呼叫 Second_bubble 函數來生成第二個 Bubble
                Third(data),   # 呼叫 Third_bubble 函數來生成第三個 Bubble
            ]
        }

        # 建立 Flex 訊息
        flex_message = FlexSendMessage(alt_text="Travel recommendations", contents=A1)

        # 回覆 Flex 訊息
        line_bot_api.reply_message(event.reply_token, flex_message)
    
    elif text_message == "不要":
        """
        存取步數到mongodb到mongodb
        """
        step = data[-1]['step']
        # mongo.insertOne(step)
        pass

    elif text_message == "不要":
        '''
        回傳不要的選項
        '''
        user_Q = '不要xxx'
        user = data['name']     
        step = data[i]['step']

        pass

    elif text_message == "情境搜索":
        # 呼叫 Vibe 函數來生成情境搜索的資料
        '''
        data = [
            {
                "placeID0": {
                    "name": "星巴克 信義南山門市",
                    "rating": 4.2,
                    "address": "110台北市信義區松仁路100號2F",
                    "url": "https://maps.app.goo.gl/rB97sxDJbqmx9UE36"
                },
                "placeID1": {
                    "name": "BUNA CAF'E 布納咖啡館 信義館",
                    "rating": 4.7,
                    "address": "110台北市信義區信義路四段415之3號",
                    "url": "https://maps.app.goo.gl/XS5FeBkM7y7zCmiGA"
                },
                "placeID2": {
                    "name": "CAFE!N 硬咖啡 吳興門市",
                    "rating": 4.2,
                    "address": "110台北市信義區吳興街8巷2號",
                    "url": "https://maps.app.goo.gl/Yid2UJkhLKvVhycJ7"
                }
            }
        ]
        '''

        # 呼叫 Vibe 函數來生成 bubble 資料
        data = recommandation(user_Q, config)
        A2 = CarouselContainer(thinking(data))

        # 建立 Flex 訊息
        flex_message = FlexSendMessage(alt_text="Vibe recommendations", contents=A2)
        
        # 回覆 Flex 訊息
        line_bot_api.reply_message(event.reply_token, flex_message)

    else:
        # 如果收到其他訊息，回覆相同的文字訊息
        line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text=f"輸入 : \n1. 情境搜索: 你想搜尋的目標 \n2. 旅遊推薦: 你想去的旅遊")
        )


# 啟動 Flask 伺服器
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
