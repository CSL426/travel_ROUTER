# mongodb_handler.py

from datetime import datetime
from typing import Dict, List, Optional
import pymongo
from pymongo.errors import PyMongoError
from .mongodb_manager import MongoDBManager


class TripDBHandler:
    """旅遊行程資料庫操作處理器

    提供所有資料庫操作的介面,包含:
    1. 規劃記錄的CRUD
    2. 用戶喜好的CRUD
    3. 其他查詢操作
    """

    def __init__(self):
        """初始化,取得資料庫連線"""
        self.db = MongoDBManager()

    def save_plan(
            self,
            line_id: str,
            input_text: str,
            requirement: Dict = None,
            itinerary: List[Dict] = None,
            feedback: Optional[List[Dict]] = None,
            restart_index: Optional[int] = None) -> int:
        """儲存規劃記錄

        Args:
            line_id: LINE用戶ID
            input_text: 用戶輸入
            requirement: 規劃需求
            itinerary: 規劃行程
            feedback: 用戶回饋(選填)
            restart_index: 重新規劃起點(選填)

        Returns:
            int: 新的plan_index

        Raises:
            PyMongoError: 儲存失敗
        """
        try:
            # 取得新的plan_index
            last_record = self.db.planner_records.find_one(
                {"line_id": line_id},
                sort=[("plan_index", pymongo.DESCENDING)]
            )
            new_index = 1 if not last_record else last_record["plan_index"] + 1

            # 建立記錄
            record = {
                "line_id": line_id,
                "plan_index": new_index,
                "timestamp": datetime.utcnow(),
                "input_text": input_text,
                "requirement": requirement,
                "itinerary": itinerary,
                "feedback": feedback,
                "restart_index": restart_index
            }

            # 移除None值
            record = {k: v for k, v in record.items() if v is not None}

            self.db.planner_records.insert_one(record)
            return new_index

        except PyMongoError as e:
            print(f"儲存規劃記錄失敗: {str(e)}")
            return None

    def update_preferences(
        self,
        line_id: str,
        preferences: Optional[Dict] = None,
        input_text: Optional[str] = None,
        profile_summary: Optional[str] = None
    ):
        """更新用戶喜好"""
        try:
            update_data = {}

            if preferences:
                preference_record = {
                    "timestamp": datetime.utcnow(),
                    **preferences
                }
                update_data["$push"] = {"preferences": preference_record}

            if input_text:
                input_record = {
                    "timestamp": datetime.utcnow(),
                    "text": input_text
                }
                update_data["$push"] = {
                    "input_history": input_record,
                    **update_data.get("$push", {})
                }

            if profile_summary:
                update_data["$set"] = {"profile_summary": profile_summary}

            if update_data:
                self.db.user_preferences.update_one(
                    {"line_id": line_id},
                    update_data,
                    upsert=True
                )

        except PyMongoError as e:
            print(f"更新用戶喜好失敗: {str(e)}")

    def get_latest_plan(self, line_id: str) -> Optional[Dict]:
        """取得最新規劃記錄"""
        try:
            return self.db.planner_records.find_one(
                {"line_id": line_id},
                sort=[("plan_index", pymongo.DESCENDING)]
            )
        except PyMongoError as e:
            print(f"取得最新規劃失敗: {str(e)}")
            return None

    def get_user_preferences(self, line_id: str) -> Optional[Dict]:
        """取得用戶喜好"""
        try:
            return self.db.user_preferences.find_one({"line_id": line_id})
        except PyMongoError as e:
            print(f"取得用戶喜好失敗: {str(e)}")
            return None

    def get_plan_by_index(self, line_id: str, plan_index: int) -> Optional[Dict]:
        """根據索引取得特定規劃記錄"""
        try:
            return self.db.planner_records.find_one({
                "line_id": line_id,
                "plan_index": plan_index
            })
        except PyMongoError as e:
            print(f"取得規劃記錄失敗: {str(e)}")
            return None

    def delete_plan(self, line_id: str, plan_index: int) -> bool:
        """刪除規劃記錄"""
        try:
            result = self.db.planner_records.delete_one({
                "line_id": line_id,
                "plan_index": plan_index
            })
            return result.deleted_count > 0
        except PyMongoError as e:
            print(f"刪除規劃記錄失敗: {str(e)}")
            return False

    def clear_user_data(self, line_id: str) -> bool:
        """清除用戶所有資料"""
        try:
            # 刪除所有規劃記錄
            self.db.planner_records.delete_many({"line_id": line_id})
            # 刪除用戶喜好
            self.db.user_preferences.delete_one({"line_id": line_id})
            return True
        except PyMongoError as e:
            print(f"清除用戶資料失敗: {str(e)}")
            return False
