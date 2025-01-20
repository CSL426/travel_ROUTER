from datetime import datetime, UTC
from typing import Dict, List, Optional
import pymongo
from pymongo.errors import PyMongoError
from .mongodb_manager import MongoDBManager


class TripDBHandler:
    """旅遊行程資料庫操作處理器

    負責:
    1. 記錄用戶輸入
    2. 儲存行程規劃
    3. 查詢歷史記錄 
    4. 錯誤處理
    """
    _instance = None  # 類別層級的變數,用來存放實例

    def __new__(cls):
        # 第一次呼叫
        if cls._instance is None:
            # 1. 用父類別的__new__建立實例
            cls._instance = super().__new__(cls)
            # 2. 初始化這個實例的db連線
            cls._instance.db = MongoDBManager()

        # 之後的呼叫都直接返回第一次建立的實例
        return cls._instance

    # def __init__(self):
    #     """初始化,取得資料庫連線"""
    #     self.db = MongoDBManager()

    def record_user_input(
        self,
        line_id: str,
        input_text: str
    ) -> bool:
        """記錄用戶輸入

        Args:
            line_id: LINE用戶ID
            input_text: 用戶輸入文字

        Returns:
            bool: 是否成功記錄
        """
        try:
            input_record = {
                "timestamp": datetime.now(UTC),
                "text": input_text
            }

            result = self.db.user_preferences.update_one(
                {"line_id": line_id},
                {"$push": {"input_history": input_record}},
                upsert=True
            )

            return result.modified_count > 0 or result.upserted_id is not None

        except PyMongoError as e:
            print(f"記錄用戶輸入失敗: {str(e)}")
            return False

    def save_plan(
        self,
        line_id: str,
        input_text: str,
        requirement: Dict,
        itinerary: List[Dict]
    ) -> Optional[int]:
        """儲存行程規劃

        Args:
            line_id: LINE用戶ID 
            input_text: 觸發規劃的輸入文字
            requirement: 規劃需求
            itinerary: 規劃行程

        Returns:
            Optional[int]: 新規劃的index,失敗時返回None
        """
        try:
            # 取得新的plan_index
            last_record = self.db.planner_records.find_one(
                {"line_id": line_id},
                sort=[("plan_index", pymongo.DESCENDING)]
            )
            new_index = 1 if not last_record else last_record["plan_index"] + 1

            # 建立規劃記錄
            record = {
                "line_id": line_id,
                "plan_index": new_index,
                "timestamp": datetime.now(UTC),
                "input_text": input_text,
                "requirement": requirement,
                "itinerary": itinerary
            }

            self.db.planner_records.insert_one(record)
            return new_index

        except PyMongoError as e:
            print(f"儲存規劃記錄失敗: {str(e)}")
            return None

    def get_input_history(
        self,
        line_id: str
    ) -> List[Dict]:
        """取得用戶輸入歷史

        Args:
            line_id: LINE用戶ID

        Returns:
            List[Dict]: 輸入記錄列表,依時間排序
        """
        try:
            user_prefs = self.db.user_preferences.find_one(
                {"line_id": line_id})
            if not user_prefs or "input_history" not in user_prefs:
                return []

            return sorted(
                user_prefs["input_history"],
                key=lambda x: x["timestamp"]
            )

        except PyMongoError as e:
            print(f"取得輸入歷史失敗: {str(e)}")
            return []

    def get_latest_plan(
        self,
        line_id: str
    ) -> Optional[Dict]:
        """取得用戶最新的規劃記錄

        Args:
            line_id: LINE用戶ID

        Returns:
            Optional[Dict]: 最新規劃記錄,無記錄時返回None
        """
        try:
            return self.db.planner_records.find_one(
                {"line_id": line_id},
                sort=[("plan_index", pymongo.DESCENDING)]
            )
        except PyMongoError as e:
            print(f"取得最新規劃失敗: {str(e)}")
            return None

    def get_plan_by_index(
        self,
        line_id: str,
        plan_index: int
    ) -> Optional[Dict]:
        """根據索引取得特定規劃記錄

        Args:
            line_id: LINE用戶ID
            plan_index: 規劃索引

        Returns:
            Optional[Dict]: 對應的規劃記錄,無記錄時返回None
        """
        try:
            return self.db.planner_records.find_one({
                "line_id": line_id,
                "plan_index": plan_index
            })
        except PyMongoError as e:
            print(f"取得規劃記錄失敗: {str(e)}")
            return None

    def clear_user_data(
        self,
        line_id: str
    ) -> bool:
        """清除用戶所有資料(測試用)

        Args:
            line_id: LINE用戶ID

        Returns:
            bool: 是否成功清除
        """
        try:
            # 刪除規劃記錄
            self.db.planner_records.delete_many({"line_id": line_id})
            # 刪除用戶偏好
            self.db.user_preferences.delete_one({"line_id": line_id})
            return True

        except PyMongoError as e:
            print(f"清除用戶資料失敗: {str(e)}")
            return False
