import os
from dotenv import load_dotenv
import pymongo
from pymongo import MongoClient
from pymongo.errors import PyMongoError


class MongoDBManager:
    """
    MongoDB連線管理

    負責:
        1. 管理資料庫連線
        2. 建立Collection
        3. 建立索引
        4. 錯誤處理
    """
    _instance = None
    _is_initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._is_initialized:
            try:
                # 載入環境變數
                load_dotenv()

                # 從環境變數取得連線字串
                MONGODB_URI = os.getenv('MONGODB_URI', "mongodb://localhost:27017")

                self.client = MongoClient(MONGODB_URI)
                self.db = self.client.travel_router

                # 建立collections
                self.planner_records = self.db.planner_records
                self.user_preferences = self.db.user_preferences

                # 建立索引
                self._create_indexes()

                MongoDBManager._is_initialized = True

            except PyMongoError as e:
                print(f"MongoDB連線失敗: {str(e)}")
                raise

    def _create_indexes(self):
        """建立所需的索引"""
        try:
            # 規劃記錄的複合索引
            self.planner_records.create_index([
                ("line_id", pymongo.ASCENDING),
                ("plan_index", pymongo.ASCENDING)
            ], unique=True)

            # 用戶喜好的索引
            self.user_preferences.create_index(
                "line_id", unique=True
            )

        except PyMongoError as e:
            print(f"建立索引失敗: {str(e)}")
            raise
