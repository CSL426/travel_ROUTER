from controller import TripController

def main():
    """測試用主程式
    提供範例輸入測試系統運作
    """
    # 初始化控制器
    controller = TripController()

    # 測試用輸入
    test_input = "想去台北文青的地方"
    print("=== 開始測試 ===")
    print(f"測試輸入: {test_input}")

    # 執行規劃
    result = controller.process_message(test_input)
    
    # 顯示結果
    print("\n=== 規劃結果 ===")
    print(result)

if __name__ == "__main__":
    main()