"""
處理LINE Bot情境搜索相關功能

負責:
1. 情境搜索請求處理
2. 收藏相關功能處理  
3. 處理其他推薦請求
"""

from linebot.v3.messaging import MessagingApi, ReplyMessageRequest, TextMessage, FlexMessage, FlexContainer
from linebot.v3.webhooks import MessageEvent
from pprint import pprint

from feature.nosql_mongo.mongo_rec.mongoDB_ctrl_disat import MongoDBManage_unsatisfied
from feature.line.rec_bubble_setting.change_format import transform_location_data
from feature.line.rec_bubble_setting.line_bubble_changer import generate_flex_messages
from main.main_plan.recommandation_service import recommandation

# 儲存狀態用的字典
user_states = {}  # 使用者狀態
recent_recommendations = {}  # 最近推薦結果
user_queries = {}  # 查詢紀錄
user_locations = {}  # 儲存用戶位置信息

class ScenarioHandler:
    """情境搜索功能處理器"""

    def __init__(self, messaging_api: MessagingApi, config: dict, logger=None):
        """初始化"""
        self.messaging_api = messaging_api
        self.config = config
        self.logger = logger

    def handle_scenario_search(self, event: MessageEvent):
        """處理情境搜索請求"""
        user_id = event.source.user_id

        try:
            # 初始化並清除舊記錄
            mongodb_obj = MongoDBManage_unsatisfied(self.config)
            mongodb_obj.delete_user_record(user_id)
            mongodb_obj.close()

            # 設定使用者狀態為等待位置
            global user_states
            user_states[user_id] = "waiting_for_location"

            # 發送請求位置訊息
            self.messaging_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="請先分享您的位置，以便我們提供更精準的推薦\n\n若不方便分享位置，請輸入「跳過」繼續使用。")]
                )
            )

        except Exception as e:
            if self.logger:
                self.logger.error(f"處理情境搜索時發生錯誤: {str(e)}")
            self._send_error_message(event.reply_token)

    def handle_location(self, event):
        """處理用戶發送的位置訊息"""
        user_id = event.source.user_id
        
        try:
            # 儲存位置資訊
            global user_locations
            user_locations[user_id] = {
                'latitude': event.message.latitude,
                'longitude': event.message.longitude
            }

            # 更新狀態為等待查詢輸入
            global user_states
            user_states[user_id] = "waiting_for_query"

            # 發送提示訊息
            self.messaging_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="已收到您的位置！\n請輸入您的需求（例如：請推薦我附近好吃的餐廳）")]
                )
            )

        except Exception as e:
            if self.logger:
                self.logger.error(f"處理位置資訊時發生錯誤: {str(e)}")
            self._send_error_message(event.reply_token)

    def handle_user_query(self, event: MessageEvent):
        """處理使用者的查詢輸入"""
        user_id = event.source.user_id
        user_text = event.message.text

        # 檢查使用者狀態
        global user_states
        if user_id not in user_states:
            return False

        # 如果正在等待位置且用戶輸入"跳過"
        if user_states[user_id] == "waiting_for_location" and user_text == "跳過":
            user_states[user_id] = "waiting_for_query"
            self.messaging_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="請輸入您的需求（例如：請推薦我好吃的餐廳）")]
                )
            )
            return True

        # 如果不是在等待查詢狀態，返回
        if user_states[user_id] != "waiting_for_query":
            return False

        # 檢查是否為特殊指令
        if user_text in ['顯示我的收藏', '推薦其他店家'] or \
           user_text.startswith('收藏店家:') or \
           user_text.startswith('移除'):
            self.messaging_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="請重新輸入您的需求")]
                )
            )
            return True

        try:
            # 清除使用者狀態
            del user_states[user_id]

            # 取得用戶位置資訊（如果有的話）
            user_location = user_locations.get(user_id, None)
            
            # 執行推薦
            final_results, query_info = recommandation(user_text, self.config, user_location)

            # 儲存查詢資訊
            query_info["line_user_id"] = user_id
            user_queries[user_id] = query_info

            # 轉換並儲存推薦結果
            transformed_data = transform_location_data(final_results)
            recent_recommendations[user_id] = transformed_data

            # 生成並發送回應
            flex_messages = generate_flex_messages(transformed_data)
            flex_message = FlexMessage(
                alt_text="為您推薦以下地點",
                contents=FlexContainer.from_dict(flex_messages)
            )
            self.messaging_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[flex_message]
                )
            )

            # 清除位置資訊
            if user_id in user_locations:
                del user_locations[user_id]

            return True

        except Exception as e:
            if self.logger:
                self.logger.error(f"處理查詢時發生錯誤: {str(e)}")
                import traceback
                self.logger.error(traceback.format_exc())
            self._send_error_message(event.reply_token)
            return True

    def _send_error_message(self, reply_token: str):
        """發送錯誤訊息"""
        try:
            self.messaging_api.reply_message(
                ReplyMessageRequest(
                    reply_token=reply_token,
                    messages=[TextMessage(text="抱歉，系統處理時發生錯誤，請稍後再試")]
                )
            )
        except Exception as e:
            if self.logger:
                self.logger.error(f"發送錯誤訊息失敗: {str(e)}")