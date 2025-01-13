# main.py

from dotenv import load_dotenv
import os
from controller import TripController


class Config:
    """系統設定類別
    負責統一管理所有API金鑰和設定
    """
    REQUIRED_KEYS = {
        'jina': ['jina_url', 'jina_headers_Authorization'],
        'qdrant': ['qdrant_url', 'qdrant_api_key'],
        'chatgpt': ['ChatGPT_api_key']
    }

    def __init__(self):
        self.config = self._load_env()
        self._validate_config()

    def _load_env(self):
        """載入環境變數"""
        config = {}
        for service in self.REQUIRED_KEYS:
            for key in self.REQUIRED_KEYS[service]:
                config[key] = os.getenv(key)
        return config

    def _validate_config(self):
        """驗證設定的完整性"""
        missing = []
        for service, keys in self.REQUIRED_KEYS.items():
            for key in keys:
                if not self.config.get(key):
                    missing.append(key)
        if missing:
            raise ValueError(f"缺少必要的設定: {', '.join(missing)}")


def init_config():
    """
    初始化設定，載入環境變數
    """
    load_dotenv()
    return {
        'jina_url': os.getenv('jina_url'),
        'jina_headers_Authorization': os.getenv('jina_headers_Authorization'),
        'qdrant_url': os.getenv('qdrant_url'),
        'qdrant_api_key': os.getenv('qdrant_api_key'),
        'ChatGPT_api_key': os.getenv('ChatGPT_api_key'),
    }


def run_trip_planner(text: str) -> str:
    """
    執行行程規劃
    """
    try:
        config = Config()

        # 建立控制器實例
        controller = TripController(config)

        # 處理輸入並取得結果
        result = controller.process_message(text)

        return result

    except Exception as e:
        return f"系統發生錯誤: {str(e)}"


if __name__ == "__main__":
    # 測試用輸入
    test_input = "想去台北文青的地方，吃午餐要便宜又好吃，下午想去逛有特色的景點，晚餐要可以跟朋友聚餐"

    # 執行規劃
    result = run_trip_planner(test_input)

    # 輸出結果
    print("=== 行程規劃結果 ===")
    print(result)
