"""
處理LINE Bot其他推薦功能

負責:
1. 處理"推薦其他店家"請求 
2. 更新推薦結果
"""

from linebot.v3.messaging import MessagingApi, ReplyMessageRequest, TextMessage, FlexMessage, FlexContainer
from linebot.v3.webhooks import MessageEvent
from feature.nosql_mongo.mongo_rec.mongoDB_ctrl_disat import MongoDBManage_unsatisfied
from feature.line.rec_bubble_setting.change_format import transform_location_data
from feature.line.rec_bubble_setting.line_bubble_changer import generate_flex_messages
from feature.line.rec_bubble_setting.query_metadata_enricher import enrich_query
from main.main_plan.rerun_reccomend import rerun_rec
from pprint import pprint


class RecommendHandler:
    """其他推薦功能處理器"""

    def __init__(self, messaging_api: MessagingApi, config: dict, logger=None):
        """初始化

        Args:
            messaging_api: LINE Bot的MessagingApi實例
            config: 設定檔內容
            logger: 可選的logger實例
        """
        self.messaging_api = messaging_api
        self.config = config
        self.logger = logger

    def recommend_others(self, event: MessageEvent,
                         recent_recommendations: dict,
                         user_queries: dict):
        """處理推薦其他店家請求

        Args:
            event: LINE message event
            recent_recommendations: 當前的推薦結果字典
            user_queries: 使用者查詢記錄字典
        """
        user_id = event.source.user_id

        try:
            # 檢查是否有前一次的推薦結果
            transformed_data = recent_recommendations.get(user_id, {})
            if not transformed_data:
                self._send_text_message(event.reply_token, "請先進行情境搜索")
                return

            # 取得所有已推薦的地點ID
            place_ids = list(transformed_data.keys())

            # 取得原始查詢資訊
            original_query = user_queries.get(user_id)
            if not original_query:
                self._send_text_message(event.reply_token, "無法找到原始查詢信息")
                return

            # 更新查詢資訊
            query_info = enrich_query(original_query, user_id, place_ids)

            # 初始化MongoDB並更新記錄
            mongodb_obj = MongoDBManage_unsatisfied(self.config)
            if mongodb_obj.test_connection():
                if not mongodb_obj.check_user_exists(user_id):
                    mongodb_obj.add_unsatisfied(query_info)
                else:
                    if mongodb_obj.compare_query(query_info):
                        mongodb_obj.update_blacklist(user_id, place_ids)
                    else:
                        mongodb_obj.update_query_info(query_info)

            # 重新運算推薦結果
            final_results, query_info = rerun_rec(query_info, self.config)

            if self.logger:
                self.logger.debug("新的推薦結果:")
                pprint(final_results, sort_dicts=False)

            # 轉換並更新推薦結果
            transformed_data = transform_location_data(final_results)
            recent_recommendations[user_id] = transformed_data

            # 生成新的回應訊息
            flex_messages = generate_flex_messages(transformed_data)
            flex_message = FlexMessage(
                alt_text="為您推薦其他地點",
                contents=FlexContainer.from_dict(flex_messages)
            )
            self.messaging_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[flex_message]
                )
            )

            mongodb_obj.close()

        except Exception as e:
            if self.logger:
                self.logger.error(f"推薦其他店家時發生錯誤: {str(e)}")
            self._send_error_message(event.reply_token)

    def _send_text_message(self, reply_token: str, text: str):
        """發送文字訊息

        Args:
            reply_token: LINE的回覆token
            text: 要發送的文字
        """
        self.messaging_api.reply_message(
            ReplyMessageRequest(
                reply_token=reply_token,
                messages=[TextMessage(text=text)]
            )
        )

    def _send_error_message(self, reply_token: str):
        """發送錯誤訊息

        Args:
            reply_token: LINE的回覆token
        """
        try:
            self.messaging_api.reply_message(
                ReplyMessageRequest(
                    reply_token=reply_token,
                    messages=[TextMessage(text="系統錯誤，請稍後再試")]
                )
            )
        except Exception as e:
            if self.logger:
                self.logger.error(f"發送錯誤訊息失敗: {str(e)}")
