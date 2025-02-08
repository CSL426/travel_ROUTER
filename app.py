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

from feature.nosql_mongo.mongo_trip.db_helper import trip_db
from main.main_trip.trip_service import run_trip_planner


# 導入情境搜索用自定義模組
from feature.nosql_mongo.mongo_rec.mongoDB_ctrl_favo import MongoDBManage_favorite
from feature.nosql_mongo.mongo_rec.mongoDB_ctrl_disat import MongoDBManage_unsatisfied
from feature.line.rec_bubble_setting.change_format import transform_location_data
from feature.line.rec_bubble_setting.line_bubble_changer import generate_flex_messages
from feature.line.rec_bubble_setting.line_bubble_favo import generate_remove_flex_messages
from main.main_plan.rerun_reccomend import rerun_rec
from feature.line.rec_bubble_setting.query_metadata_enricher import enrich_query
from main.main_plan.recommandation_service import recommandation

# 情境搜索用全局變數
user_states = {}  # 儲存用戶當前狀態的字典
recent_recommendations = {}  # 儲存用戶最近一次的推薦結果
user_queries = {}  # 儲存用戶的查詢資訊

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


def create_rich_menu():
    import requests
    import io
    from linebot.v3.messaging.models import (
        RichMenuRequest,
        RichMenuArea,
        RichMenuBounds,
        RichMenuSize,
        MessageAction,
    )
    from PIL import Image, ImageDraw, ImageFont
    import os
    api_client = ApiClient(configuration)
    messaging_api = MessagingApi(api_client)
    script_dir = os.path.dirname(os.path.abspath(__file__))  # 獲取當前腳本的目錄
    font_path = os.path.join(script_dir, 'data/fonts', 'mingliu.ttc')  # 字型檔案的相對路徑
    # 使用相對路徑加載字型
    font = ImageFont.truetype(font_path, 120)
    """創建 LINE 的圖文選單"""
    rich_menu = RichMenuRequest(
        size=RichMenuSize(width=2500, height=843),
        selected=True,
        name="Main Menu",
        chat_bar_text="點擊開啟選單",
        areas=[
            RichMenuArea(
                bounds=RichMenuBounds(x=0, y=0, width=1250, height=843),
                action=MessageAction(text="我想進行情境搜索", label="情境搜索")
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=1250, y=0, width=1250, height=843),
                action=MessageAction(text="顯示我的收藏", label="我的收藏")
            )
        ]
    )

    rich_menu_id = messaging_api.create_rich_menu(rich_menu_request=rich_menu)
    
    # 創建選單圖片
    img = Image.new('RGB', (2500, 843), '#ffffff')
    draw = ImageDraw.Draw(img)
    draw.text((625, 421), "情境搜索", fill='black', anchor='mm', font=font)
    draw.text((1875, 421), "我的收藏", fill='black', anchor='mm', font=font)
    
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    url = f'https://api-data.line.me/v2/bot/richmenu/{rich_menu_id.rich_menu_id}/content'
    headers = {
        'Authorization': f'Bearer {LINE_CHANNEL_ACCESS_TOKEN}',
        'Content-Type': 'image/png'
    }
    requests.post(url, headers=headers, data=img_byte_arr)
    
    messaging_api.set_default_rich_menu(rich_menu_id=rich_menu_id.rich_menu_id)
create_rich_menu()


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
            messaging_api = MessagingApi(api_client)
            
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
                        First(data)
                    ]
                }

                flex_message = FlexMessage(
                    alt_text="Travel recommendations",
                    contents=FlexContainer.from_dict(A1)
                )

                messaging_api.reply_message_with_http_info(
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
                
                messaging_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text=message_text)]
                    )
                )


    except Exception as e:
        app.logger.error(f"Error handling message: {str(e)}")
        # 發生錯誤時，嘗試傳送錯誤訊息給使用者
        try:
            with ApiClient(configuration) as api_client:
                messaging_api = MessagingApi(api_client)
                messaging_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text="處理訊息時發生錯誤，請稍後再試")]
                    )
                )
        except Exception as inner_e:
            app.logger.error(f"Error sending error message: {str(inner_e)}")

    # ======================================================以下是情境搜索
    api_client = ApiClient(configuration)
    messaging_api = MessagingApi(api_client)

    """處理用戶發送的訊息"""
    user_id = event.source.user_id

    if event.message.text == "我想進行情境搜索":

        # 初始化 MongoDB 管理器
        mongodb_obj = MongoDBManage_unsatisfied(config)
        
        # 清除該用戶之前的記錄
        mongodb_obj.delete_user_record(user_id)
        mongodb_obj.close()
        
        # 設定用戶狀態為等待查詢
        user_states[user_id] = "waiting_for_query"
        messaging_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text="請輸入你的需求(例如:請推薦我淡水好吃的餐廳)")]
            )
        )

    elif user_id in user_states and user_states[user_id] == "waiting_for_query":
        while event.message.text in ['顯示我的收藏','推薦其他店家'] or event.message.text[0:4] == '收藏店家'or event.message.text[0:2] == '移除':
            messaging_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text="請重新輸入你的需求(例如:請推薦我淡水好吃的餐廳)")]
                )
            )

        try:
            # 清除用戶狀態
            del user_states[user_id]
            
            # 執行推薦
            final_results, query_info = recommandation(event.message.text, config)
            from pprint import pprint
            pprint(final_results, sort_dicts=False)


            # 儲存查詢資訊
            query_info["line_user_id"] = user_id
            user_queries[user_id] = query_info

            # 轉換資料格式並儲存
            transformed_data = transform_location_data(final_results)
            recent_recommendations[user_id] = transformed_data

            # 生成 Flex 消息
            flex_messages = generate_flex_messages(transformed_data)

            flex_message = FlexMessage(
                alt_text="為您推薦以下地點",
                contents=FlexContainer.from_dict(flex_messages)
            )
            
            # 發送消息
            messaging_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[flex_message]
                )
            )
            
        except Exception as e:
            import traceback
            print(f"處理查詢時發生錯誤: {e}")
            print("錯誤詳細信息:")
            print(traceback.format_exc())
            messaging_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="抱歉，系統處理時發生錯誤，請稍後再試")]
                )
            )
        return

    elif event.message.text == "顯示我的收藏":
        try:
            mongodb_obj = MongoDBManage_favorite(config)
            
            if mongodb_obj.check_user(user_id):
                favorites = mongodb_obj.show_favorite(user_id)
                if favorites:
                    flex_messages, _ = generate_remove_flex_messages(favorites, user_id)
                    
                    flex_message = FlexMessage(
                        alt_text="您的收藏清單",
                        contents=FlexContainer.from_dict(flex_messages)
                    )
                    
                    messaging_api.reply_message(
                        ReplyMessageRequest(
                            reply_token=event.reply_token,
                            messages=[flex_message]
                        )
                    )
                else:
                    messaging_api.reply_message(
                        ReplyMessageRequest(
                            reply_token=event.reply_token,
                            messages=[TextMessage(text="您的收藏夾是空的")]
                        )
                    )
            else:
                messaging_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text="您沒有收藏任何點位")]
                    )
                )
            
            mongodb_obj.close()
            
        except Exception as e:
            print(f"MongoDB 操作錯誤: {e}")
            messaging_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="系統錯誤，請稍後再試")]
                )
            )
    
    elif event.message.text.startswith("收藏店家:"):
        try:
            place_name = event.message.text.split(":")[1]
            
            # 從用戶的最近推薦結果中查找地點資訊
            transformed_data = recent_recommendations.get(user_id, {})
            place_info = None
            place_id = None
            
            # 遍歷字典查找匹配的地點
            for pid, place in transformed_data.items():
                if place["name"] == place_name:
                    place_info = place
                    place_id = pid
                    break

            if place_info:
                # 準備要存入 MongoDB 的資料格式
                place_data = {
                    "name": place_info["name"],
                    "rating": place_info["rating"],
                    "address": place_info["address"],
                    "location_url": place_info.get("location_url", f"https://www.google.com/maps/place/?q=place_id:{place_id}"),
                    "image_url": place_info.get("image_url", "")
                }
                
                # 初始化 MongoDB 管理器
                mongodb_obj = MongoDBManage_favorite(config)
                
                if mongodb_obj.check_user(user_id):
                    if mongodb_obj.check_place(user_id, place_id):
                        message_text = f"已收藏過: {place_name}"
                    else:
                        if mongodb_obj.fix_favorite(user_id, place_id, place_data):
                            message_text = f"已收藏 {place_name}"
                        else:
                            message_text = "收藏失敗，請稍後再試"
                else:
                    if mongodb_obj.add_user(user_id, place_id, place_data):
                        message_text = f"已收藏 {place_name}"
                    else:
                        message_text = "收藏失敗，請稍後再試"
                
                mongodb_obj.close()
            else:
                message_text = "找不到該地點的資訊"
                
        except Exception as e:
            print(f"收藏操作錯誤: {e}")
            message_text = "系統錯誤，請稍後再試"
            
        messaging_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=message_text)]
            )
        )
            
        # 處理再推薦的部分
    elif event.message.text == "推薦其他店家":
        try:
            # 1. 從 recent_recommendations 中獲取當前的推薦結果
            transformed_data = recent_recommendations.get(user_id, {})
            if not transformed_data:
                messaging_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text="請先進行情境搜索")]
                    )
                )
                return

            # 2. 獲取所有推薦地點的 ID
            place_ids = list(transformed_data.keys())

            # 3. 從 user_queries 獲取原始查詢信息
            original_query = user_queries.get(user_id)
            if not original_query:
                messaging_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text="無法找到原始查詢信息")]
                    )
                )
                return

            # 4. 使用 enrich_query 更新查詢信息
            query_info = enrich_query(original_query, user_id, place_ids)

            # 5. 初始化 MongoDB 管理器
            mongodb_obj = MongoDBManage_unsatisfied(config)

            # 6. 檢查用戶是否存在並進行相應操作
            if mongodb_obj.test_connection():
                if not mongodb_obj.check_user_exists(user_id):
                    # 新用戶，添加記錄
                    mongodb_obj.add_unsatisfied(query_info)
                else:
                    # 已存在的用戶，比較查詢
                    if mongodb_obj.compare_query(query_info):
                        # 相同查詢，更新黑名單
                        mongodb_obj.update_blacklist(user_id, place_ids)
                    else:
                        # 不同查詢，更新查詢信息
                        mongodb_obj.update_query_info(query_info)

            # 7. 重新運算推薦結果
            final_results, query_info = rerun_rec(query_info, config)
            
            from pprint import pprint
            print('========================')
            pprint(final_results, sort_dicts=False)
            print('========================')

            # 8. 轉換並更新推薦結果
            transformed_data = transform_location_data(final_results)
            recent_recommendations[user_id] = transformed_data

            # 9. 生成新的 Flex 消息
            flex_messages = generate_flex_messages(transformed_data)
            
            flex_message = FlexMessage(
                alt_text="為您推薦其他地點",
                contents=FlexContainer.from_dict(flex_messages)
            )
            
            # 10. 發送新的推薦結果
            messaging_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[flex_message]
                )
            )

            mongodb_obj.close()

        except Exception as e:
            print(f"再推薦處理錯誤: {e}")
            messaging_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="抱歉，重新推薦時發生錯誤，請稍後再試")]
                )
            )
            
    elif event.message.text.startswith("移除"):
        try:
            place_name = event.message.text[2:]  # 去掉"移除"兩個字
            
            mongodb_obj = MongoDBManage_favorite(config)
            
            # 獲取用戶的收藏來找到對應的 place_id
            favorites = mongodb_obj.show_favorite(user_id)
            if favorites:
                place_id = next((pid for pid, data in favorites.items() 
                               if data["name"] == place_name), None)
                
                if place_id:
                    print(f"用戶ID: {user_id}\n地點ID: {place_id}")  # 後端輸出
                    if mongodb_obj.delete_favorite(user_id, place_id):
                        message_text = f"已刪除: {place_name}"
                    else:
                        message_text = "刪除失敗，請稍後再試"
                else:
                    message_text = "找不到該收藏"
            else:
                message_text = "您沒有任何收藏"
            
            mongodb_obj.close()
            
        except Exception as e:
            print(f"MongoDB 操作錯誤: {e}")
            message_text = "系統錯誤，請稍後再試"
        
        messaging_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=message_text)]
            )
        )


if __name__ == "__main__":
    app.run(debug=False,host="0.0.0.0", port=8080)