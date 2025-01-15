# main.py

from dotenv import load_dotenv
import os

from main.main_trip.controllers.controller import TripController, init_config


def run_trip_planner(text: str) -> str:
    """執行行程規劃

    輸入:
        text: str - 使用者輸入的需求描述
              例如: "想去台北文青的地方，午餐要吃美食"

    回傳:
        str - 完整的行程規劃結果
    """
    try:
        controller_instance = TripController(init_config())

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
    a = 1
