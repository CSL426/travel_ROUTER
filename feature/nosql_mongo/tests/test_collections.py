import os
from dotenv import load_dotenv
import pytest
from pymongo import MongoClient
from pymongo.errors import PyMongoError

from feature.nosql_mongo.mongo_trip.mongodb_manager import MongoDBManager


def test_connection():
    """測試MongoDB連線"""
    try:
        # 載入環境變數
        load_dotenv()

        # 從環境變數取得連線字串,如果沒有就用localhost
        MONGODB_URI = os.getenv('MONGODB_URI', "mongodb://localhost:27017")

        # 建立連線
        client = MongoClient(MONGODB_URI)

        # 測試連線
        client.server_info()
        print("\n成功連線到MongoDB!")

        # 列出所有資料庫
        databases = client.list_database_names()
        print("\n已有的資料庫:")
        for db in databases:
            print(f"- {db}")

        # 選擇travel_planner資料庫
        db = client.travel_planner

        # 列出該資料庫的collections
        collections = db.list_collection_names()
        print("\ntravel_planner資料庫中的collections:")
        for collection in collections:
            print(f"- {collection}")
            # 列出該collection的document數量
            count = db[collection].count_documents({})
            print(f"  文件數量: {count}")

            # 印出一個範例文件
            if count > 0:
                example = db[collection].find_one()
                print(f"  範例文件:")
                print(f"  {example}")

    except PyMongoError as e:
        pytest.fail(f"MongoDB連線失敗: {str(e)}")


def test_mongodb_manager():
    """測試MongoDBManager"""
    try:
        # 初始化manager
        manager = MongoDBManager()

        # 確認collections已建立
        assert hasattr(manager, 'planner_records')
        assert hasattr(manager, 'user_preferences')
        print("\nMongoDBManager初始化成功!")

        # 列出已建立的索引
        print("\nplanner_records的索引:")
        for index in manager.planner_records.list_indexes():
            print(f"- {index}")

        print("\nuser_preferences的索引:")
        for index in manager.user_preferences.list_indexes():
            print(f"- {index}")

    except PyMongoError as e:
        pytest.fail(f"MongoDBManager測試失敗: {str(e)}")


def test_crud_operations():
    """測試基本的CRUD操作"""
    try:
        # 使用測試資料
        test_data = {
            "line_id": "test_user",
            "input_text": "測試輸入",
            "requirement": {"test": "requirement"},
            "itinerary": [{"test": "itinerary"}]
        }

        # 初始化manager
        manager = MongoDBManager()

        # Create: 插入測試資料
        result = manager.planner_records.insert_one(test_data)
        inserted_id = result.inserted_id
        print(f"\n插入的文件ID: {inserted_id}")

        # Read: 讀取插入的資料
        found = manager.planner_records.find_one({"_id": inserted_id})
        print(f"\n讀取的文件:")
        print(found)

        # Update: 更新資料
        update_result = manager.planner_records.update_one(
            {"_id": inserted_id},
            {"$set": {"input_text": "更新的測試輸入"}}
        )
        print(f"\n更新結果:")
        print(f"符合條件的文件數: {update_result.matched_count}")
        print(f"實際更新的文件數: {update_result.modified_count}")

        # 確認更新結果
        updated = manager.planner_records.find_one({"_id": inserted_id})
        print(f"\n更新後的文件:")
        print(updated)

        # Delete: 刪除測試資料
        delete_result = manager.planner_records.delete_one(
            {"_id": inserted_id})
        print(f"\n刪除結果:")
        print(f"刪除的文件數: {delete_result.deleted_count}")

    except PyMongoError as e:
        pytest.fail(f"CRUD操作測試失敗: {str(e)}")


if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])
