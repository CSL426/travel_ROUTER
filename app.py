from dotenv import dotenv_values
from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    FlexMessage,
    FlexContainer,
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

from feature.line.bubbles_seting.First_bubble import First
from feature.line.bubbles_seting.Second_bubble import Second
from feature.line.bubbles_seting.Third_bubble import Third
from feature.line.Vibe import thinking  # 載入 Vibe 函數

from feature.nosql_mongo.mongo_trip.db_helper import trip_db
from main.main_trip.trip_service import run_trip_planner
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

# 初始化 Configuration 和 WebhookHandler
configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

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

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    text_message = event.message.text

    try:
        line_id = event.source.user_id
    except Exception:
        line_id = 'none_line_id'
    
    trip_db.record_user_input(line_id, text_message)
    original_text_message = text_message
    user_Q = text_message[5:]
    text_message = text_message[0:4]

    try:
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            
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
                data = run_trip_planner(text=user_Q, line_id=line_id)
                A1 = {
                    "type": "carousel",
                    "contents": [
                        First(data),
                        Second(data)
                    ]
                }

                flex_message = FlexMessage(
                    alt_text="Travel recommendations",
                    contents=FlexContainer.from_dict(A1)
                )

                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[flex_message]
                    )
                )

            elif original_text_message[0:5] == "資料初始化":
                """
                清除用戶所有資料
                """
                if len(original_text_message) > 5:
                    line_id = original_text_message[5:].strip()
                
                success = trip_db.clear_user_data(line_id)
                
                message_text = "初始化成功" if success else "初始化錯誤，請稍後再試"
                
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text=message_text)]
                    )
                )

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
                # 獲取推薦結果和查詢信息
                results, query_info = recommandation(user_Q, config)
                
                # 更新 query_info 中的 line_user_id
                query_info['line_user_id'] = line_id
                
                A2 = {
                    "type": "carousel",
                    "contents": thinking(results)
                }

                flex_message = FlexMessage(
                    alt_text="Vibe recommendations",
                    contents=FlexContainer.from_dict(A2)
                )
                # 回覆 Flex 訊息
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[flex_message]
                    )
                )

            else:
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text=f"輸入 : \n1. 情境搜索: 你想搜尋的目標 \n2. 旅遊推薦: 你想去的旅遊")]
                    )
                )

    except Exception as e:
        app.logger.error(f"Error handling message: {str(e)}")
        # 發生錯誤時，嘗試傳送錯誤訊息給使用者
        try:
            with ApiClient(configuration) as api_client:
                line_bot_api = MessagingApi(api_client)
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text="處理訊息時發生錯誤，請稍後再試")]
                    )
                )
        except Exception as inner_e:
            app.logger.error(f"Error sending error message: {str(inner_e)}")

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8787)
