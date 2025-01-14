# main.py

from dotenv import load_dotenv
import os

from main.main_trip.controller import TripController


def init_config():
    """初始化設定

    載入環境變數並整理成設定字典

    回傳:
        dict: 包含所有 API 設定的字典，包括:
            - jina_url: Jina API 端點
            - jina_headers_Authorization: Jina 認證金鑰
            - qdrant_url: Qdrant 伺服器位址
            - qdrant_api_key: Qdrant 存取金鑰
            - ChatGPT_api_key: OpenAI API 金鑰
    """
    # 直接載入環境變數，這樣在容器中也能正常運作
    load_dotenv()

    config = {
        'jina_url': os.getenv('jina_url'),
        'jina_headers_Authorization': os.getenv('jina_headers_Authorization'),
        'qdrant_url': os.getenv('qdrant_url'),
        'qdrant_api_key': os.getenv('qdrant_api_key'),
        'ChatGPT_api_key': os.getenv('ChatGPT_api_key')
    }

    # 驗證所有設定都存在
    missing = [key for key, value in config.items() if not value]
    if missing:
        raise ValueError(f"缺少必要的API設定: {', '.join(missing)}")

    return config


def run_trip_planner(text: str) -> str:
    """執行行程規劃

    輸入:
        text: str - 使用者輸入的需求描述
              例如: "想去台北文青的地方，午餐要吃美食"

    回傳:
        str - 完整的行程規劃結果
    """
    try:
        print("DEBUG: Starting run_trip_planner")
        config = init_config()
        print("DEBUG: Config initialized:", bool(config))

        print("DEBUG: About to create TripController")

        controller_instance = TripController(config)
        print("DEBUG: TripController created")

        result = controller_instance.process_message(text)
        controller_instance.trip_planner.print_itinerary(
            result,
        )
        return result

    except Exception as e:
        print("DEBUG: Exception details:", str(e))  # 完整錯誤訊息
        return f"系統發生錯誤: {str(e)}"


if __name__ == "__main__":
    test_input = "想去台北文青的地方，吃午餐要便宜又好吃，下午想去逛有特色的景點，晚餐要可以跟朋友聚餐"
    result = run_trip_planner(test_input)
