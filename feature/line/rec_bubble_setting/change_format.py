import pandas as pd
pd.options.mode.copy_on_write = True

def transform_location_data(input_data):
    """
    將 Location 資料從輸入格式轉換為所需的輸出格式
    只需要輸入包含 placeID 的資料，其他資訊會從 CSV 自動補充
    
    參數:
        input_data (list): 包含地點資訊的列表，每個元素至少要有 placeID
        
    回傳:
        dict: 轉換後的資料格式，以 placeID 為鍵的字典
    """
    try:
        # 讀取CSV資料
        df = pd.read_csv('./data/ETL_dataframe.csv')
        
        transformed = {}
        for location in input_data:
            # 取得 placeID
            place_id = location.get('placeID')
            if not place_id:
                continue
            
            # 從 CSV 找到對應資料
            place_data = df[df['place_id'] == place_id]
            if len(place_data) == 0:
                print(f"警告：找不到 placeID {place_id} 的資料")
                continue
            
            place_data = place_data.iloc[0]
            
            # 建立資料字典
            transformed[place_id] = {
                'name': place_data.get('place_name', ''),
                'rating': float(place_data.get('rating', 0.0)),
                'address': place_data.get('address', ''),
                'location_url': f"https://www.google.com/maps/place/?q=place_id:{place_id}",
                'image_url': place_data.get('image_url', '')
            }
            
        return transformed
        
    except Exception as e:
        print(f"讀取或轉換資料時發生錯誤: {e}")
        return {}

# 測試用
if __name__ == "__main__":
    # 測試數據 - 使用真實的 place IDs
    test_data = [
        {'placeID': 'ChIJf4zdZN2oQjQRxGBrtbxWJ1o'},  # 淡水一家店
        {'placeID': 'ChIJF5VTuRumQjQRyAT4V-4-hxI'}   # 淡水另一家店
    ]
    
    # 測試轉換
    result = transform_location_data(test_data)
    print("轉換結果：")
    for place_id, info in result.items():
        print(f"\n{place_id}:")
        for key, value in info.items():
            print(f"  {key}: {value}")