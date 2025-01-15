import sys
import os
import pandas as pd
import numpy as np
from geopy.distance import geodesic
import math

def run_test(results, user_demand_list):
    print("Input results:", results)  # Debug: 檢查輸入數據
    print("Input user_demand:", user_demand_list)  # Debug: 檢查用戶需求
    
    # 權重定義
    weights = {
        "price": 0.4,
        "distance": 0.3,
        "rating": 0.2,
        "match": 0.1
    }
    
    # 取得專案根目錄的路徑
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    database_path = os.path.join(project_root, 'database')
    
    # 初始過濾結果清單
    filtered_results = []
    
    # 取得用戶需求
    if isinstance(user_demand_list, list) and len(user_demand_list) > 0:
        user_demand = user_demand_list[0]
    else:
        user_demand = user_demand_list

    # 時間資料路徑
    transformed_df_path = os.path.join(database_path, 'transformed_df.csv')
    try:
        condition_hours = pd.read_csv(transformed_df_path)
    except FileNotFoundError:
        print("警告：找不到時間資料檔案，將跳過時間檢查")
        condition_hours = pd.DataFrame()

    # 基本過濾
    for condition in results:
        match_score = condition.get('match_score', 0)
        
        # 檢查類別
        if user_demand.get('類別', 'none') != 'none':
            place_type = condition.get('label_type')
            user_type = user_demand['類別']
            print(f"Checking place: {condition.get('name')} - Type: {place_type} vs Required: {user_type}")  # Debug
            
            # 修改: 處理 None 或 nan 的情況
            if pd.isna(place_type) or place_type is None:
                continue
                
            # 增加模糊匹配
            if not (place_type.strip() == user_type.strip() or
                   user_type.strip() in place_type.strip() or
                   place_type.strip() in user_type.strip()):
                print(f"Skipping {condition.get('name')} due to type mismatch")  # Debug
                continue

        condition['match_score'] = match_score
        filtered_results.append(condition)
        print(f"Added {condition.get('name')} to filtered results")  # Debug

    print(f"Filtered results count: {len(filtered_results)}")  # Debug
    if not filtered_results:
        print("No places matched the criteria")  # Debug
        return []

    # 計算評分所需的最大最小值
    distances = [condition.get('distance', 0) for condition in filtered_results]
    min_distance = min(distances) if distances else 0
    max_distance = max(distances) if distances else 1

    # 過濾有效價格，處理 None 和 nan 的情況
    valid_prices = []
    for c in filtered_results:
        price = c.get('avg_cost')
        if price is not None and not pd.isna(price):
            try:
                valid_prices.append(float(price))
            except (ValueError, TypeError):
                continue

    min_price = min(valid_prices) if valid_prices else 0
    max_price = max(valid_prices) if valid_prices else 1

    max_reviews = max([c.get('num_comments', 0) for c in filtered_results])

    # 計算各項分數
    for condition in filtered_results:
        # 價格分數
        if pd.isna(condition.get('avg_cost')):
            condition['price_score'] = 5
        else:
            price = float(condition['avg_cost'])
            condition['price_score'] = (10 * (1 - (price - min_price) / (max_price - min_price)) 
                                      if max_price > min_price else 10)

        # 距離分數
        distance = condition.get('distance', 0)
        condition['distance_score'] = (10 * (1 - (distance - min_distance) / (max_distance - min_distance))
                                     if max_distance > min_distance else 10)

        # 評分分數
        rating = condition.get('rating', 0)
        reviews = condition.get('num_comments', 0)
        condition['rating_score'] = ((rating * 2) + (math.log(reviews + 1) / math.log(max_reviews + 1) * 5)
                                   if rating > 0 and reviews > 0 else 0)

        # 匹配分數
        condition['match_score'] = condition.get('match_score', 0) * 10

        # 總分計算
        condition['total_score'] = (
            condition['price_score'] * weights['price'] +
            condition['distance_score'] * weights['distance'] +
            condition['rating_score'] * weights['rating'] +
            condition['match_score'] * weights['match']
        )

    # 排序並選取前15名
    sorted_results = sorted(filtered_results, key=lambda x: x.get('total_score', 0), reverse=True)[:15]

    # 準備輸出結果
    output_list = []
    for condition in sorted_results:
        output_dict = {
            'place_id': condition.get('place_id'),
            'name': condition.get('name'),
            'rating': condition.get('rating'),
            'num_comments': condition.get('num_comments'),
            'avg_cost': condition.get('avg_cost'),
            'label_type': condition.get('label_type'),
            'hours': condition.get('hours'),
            'total_score': condition.get('total_score')
        }
        output_list.append(output_dict)

    # Debug輸出
    print("推薦如下：")
    for condition in output_list:
        print(f"{condition['name']}: 總分 {condition['total_score']}")

    return output_list

if __name__ == "__main__":
    three = [{'place_id': 'ChIJ_5boPdypQjQRPAGE671e1ys', 'name': '育圃安親課輔 | 親子共學空間', 'rating': 5.0, 'num_comments': 6, 'lon': 121.5099975, 'lat': 25.0012258, 'avg_cost': np.nan, 'label_type': '餐廳', 'label': '補習班', 'hours': "{1: [{'start': '09:00', 'end': '21:00'}], 2: [{'start': '09:00', 'end': '21:00'}], 3: [{'start': '09:00', 'end': '21:00'}], 4: [{'start': '09:00', 'end': '21:00'}], 5: [{'start': '09:00', 'end': '21:00'}], 6: 'none', 7: 'none'}", 'match_score': 0.53607726, 'url': 'https://www.google.com/maps/place/?q=place_id:ChIJ_5boPdypQjQRPAGE671e1ys'}, {'place_id': 'ChIJ_4-qS0hTXTQR-oEnlnTcouU', 'name': '桶Q紫米飯團', 'rating': 5.0, 'num_comments': 6, 'lon': 121.6408579, 'lat': 25.0645388, 'avg_cost': 150.0, 'label_type': '餐廳', 'label': '早餐餐廳', 'hours': "{1: [{'start': '06:00', 'end': '12:00'}], 2: [{'start': '06:00', 'end': '12:00'}], 3: 'none', 4: [{'start': '06:00', 'end': '12:00'}], 5: [{'start': '06:00', 'end': '12:00'}], 6: [{'start': '06:00', 'end': '13:00'}], 7: [{'start': '06:00', 'end': '13:00'}]}", 'match_score': 0.50490946, 'url': 'https://www.google.com/maps/place/?q=place_id:ChIJ_4-qS0hTXTQR-oEnlnTcouU'}, {'place_id': 'ChIJ__-vgaWrQjQR2HPcrD3KZ74', 'name': '衣衫二像', 'rating': 5.0, 'num_comments': 1, 'lon': 121.5768118, 'lat': 25.0403936, 'avg_cost': np.nan, 'label_type': '購物商場', 'label': '服裝店', 'hours': "{1: [{'start': '11:00', 'end': '21:00'}], 2: [{'start': '11:00', 'end': '21:00'}], 3: [{'start': '11:00', 'end': '21:00'}], 4: [{'start': '11:00', 'end': '21:00'}], 5: [{'start': '11:00', 'end': '21:00'}], 6: [{'start': '12:00', 'end': '19:00'}], 7: 'none'}", 'match_score': 0.5492884, 'url': 'https://www.google.com/maps/place/?q=place_id:ChIJ__-vgaWrQjQR2HPcrD3KZ74'}, {'place_id': 'ChIJ_1RbiZCvQjQRHWDwJSOks4U', 'name': '大八里豬腸冬粉專賣店', 'rating': 5.0, 'num_comments': 2, 'lon': 121.4481135, 'lat': 25.1403297, 'avg_cost': np.nan, 'label_type': '小吃', 'label': '熟食店', 'hours': "{1: [{'start': '06:00', 'end': '14:00'}], 2: [{'start': '06:00', 'end': '14:00'}], 3: [{'start': '06:00', 'end': '14:00'}], 4: [{'start': '06:00', 'end': '14:00'}], 5: [{'start': '06:00', 'end': '14:00'}], 6: [{'start': '06:00', 'end': '14:00'}], 7: [{'start': '06:00', 'end': '14:00'}]}", 'match_score': 0.42361003, 'url': 'https://www.google.com/maps/place/?q=place_id:ChIJ_1RbiZCvQjQRHWDwJSOks4U'}, {'place_id': 'ChIJ_2li6YGnQjQR2HW9HwFSBgY', 'name': '美 鳳麵線1號店', 'rating': 5.0, 'num_comments': 44, 'lon': 121.4375529, 'lat': 25.08253, 'avg_cost': 150.0, 'label_type': '餐廳', 'label': '早午餐餐廳', 'hours': "{1: 'none', 2: [{'start': '06:00', 'end': '13:00'}], 3: [{'start': '06:00', 'end': '13:00'}], 4: [{'start': '06:00', 'end': '13:00'}], 5: [{'start': '06:00', 'end': '13:00'}], 6: [{'start': '06:00', 'end': '13:30'}], 7: [{'start': '06:00', 'end': '13:30'}]}", 'match_score': 0.3645823, 'url': 'https://www.google.com/maps/place/?q=place_id:ChIJ_2li6YGnQjQR2HW9HwFSBgY'}, {'place_id': 'ChIJ_7TmjcQDaDQR0hzmnCdj0hA', 'name': 'World Gym世界健身俱樂部 新北 土城海山店Sport(預售中心)', 'rating': 4.9, 'num_comments': 827, 'lon': 121.4436785, 'lat': 24.9834888, 'avg_cost': np.nan, 'label_type': '休閒設施', 'label': '健身室', 'hours': "{1: [{'start': '10:00', 'end': '00:00'}], 2: [{'start': '10:00', 'end': '00:00'}], 3: [{'start': '10:00', 'end': '00:00'}], 4: [{'start': '10:00', 'end': '00:00'}], 5: [{'start': '10:00', 'end': '00:00'}], 6: [{'start': '10:00', 'end': '00:00'}], 7: [{'start': '10:00', 'end': '00:00'}]}", 'match_score': 0.4299067, 'url': 'https://www.google.com/maps/place/?q=place_id:ChIJ_7TmjcQDaDQR0hzmnCdj0hA'}, {'place_id': 'ChIJ_3LZiLyvQjQR3SvEA0zV4Hk', 'name': '大俠請留步', 'rating': 4.8, 'num_comments': 3316, 'lon': 121.5271151, 'lat': 25.0897344, 'avg_cost': 500.0, 'label_type': '餐廳', 'label': '餐廳', 'hours': "{1: 'none', 2: [{'start': '17:00', 'end': '00:00'}], 3: [{'start': '17:00', 'end': '00:00'}], 4: [{'start': '17:00', 'end': '00:00'}], 5: [{'start': '17:00', 'end': '00:00'}], 6: [{'start': '17:00', 'end': '00:00'}], 7: [{'start': '17:00', 'end': '00:00'}]}", 'match_score': 0.53327787, 'url': 'https://www.google.com/maps/place/?q=place_id:ChIJ_3LZiLyvQjQR3SvEA0zV4Hk'}, {'place_id': 'ChIJ_1wySmGpQjQRHjQAQyBy8Eo', 'name': '百大安師補習班長安旗艦校', 'rating': 4.8, 'num_comments': 206, 'lon': 121.5315931, 'lat': 25.0511646, 'avg_cost': np.nan, 'label_type': np.nan, 'label': '補習班', 'hours': "{1: [{'start': '15:00', 'end': '22:00'}], 2: [{'start': '15:00', 'end': '22:00'}], 3: 'none', 4: [{'start': '15:00', 'end': '22:00'}], 5: [{'start': '15:00', 'end': '22:00'}], 6: [{'start': '08:30', 'end': '17:00'}], 7: 'none'}", 'match_score': 0.41600662, 'url': 'https://www.google.com/maps/place/?q=place_id:ChIJ_1wySmGpQjQRHjQAQyBy8Eo'}, {'place_id': 'ChIJ_2DulyADaDQR03uIlrJIGbg', 'name': '叡製手作豆花', 'rating': 4.8, 'num_comments': 79, 'lon': 121.4999193, 'lat': 24.9923188, 'avg_cost': 150.0, 'label_type': '甜品店/飲料店', 'label': '甜品店', 'hours': "{1: [{'start': '15:00', 'end': '21:00'}], 2: [{'start': '15:00', 'end': '21:00'}], 3: [{'start': '15:00', 'end': '21:00'}], 4: [{'start': '15:00', 'end': '21:00'}], 5: [{'start': '15:00', 'end': '21:00'}], 6: [{'start': '15:00', 'end': '21:00'}], 7: 'none'}", 'match_score': 0.47897473, 'url': 'https://www.google.com/maps/place/?q=place_id:ChIJ_2DulyADaDQR03uIlrJIGbg'}, {'place_id': 'ChIJ_3qhwzWrQjQR9qdg6STTZHI', 'name': '肉老大頂級肉品涮涮鍋 蘆洲火鍋店', 'rating': 4.8, 'num_comments': 2975, 'lon': 121.460375, 'lat': 25.081996, 'avg_cost': 500.0, 'label_type': '餐廳', 'label': '火鍋餐廳', 'hours': "{1: [{'start': '11:30', 'end': '01:30'}], 2: [{'start': '11:30', 'end': '01:30'}], 3: [{'start': '11:30', 'end': '01:30'}], 4: [{'start': '11:30', 'end': '01:30'}], 5: [{'start': '11:30', 'end': '01:30'}], 6: [{'start': '11:30', 'end': '01:30'}], 7: [{'start': '11:30', 'end': '01:30'}]}", 'match_score': 0.49828416, 'url': 'https://www.google.com/maps/place/?q=place_id:ChIJ_3qhwzWrQjQR9qdg6STTZHI'}, {'place_id': 'ChIJ_3Drk2CpQjQRj60tccm_S-c', 'name': '藝鍋物-板橋三民店', 'rating': 4.7, 'num_comments': 1085, 'lon': 121.4792924, 'lat': 25.0221787, 'avg_cost': 300.0, 'label_type': ' 餐廳', 'label': '火鍋餐廳', 'hours': "{1: [{'start': '11:00', 'end': '14:00'}, {'start': '17:00', 'end': '22:00'}], 2: [{'start': '11:00', 'end': '14:00'}, {'start': '17:00', 'end': '22:00'}], 3: [{'start': '11:00', 'end': '14:00'}, {'start': '17:00', 'end': '22:00'}], 4: [{'start': '11:00', 'end': '14:00'}, {'start': '17:00', 'end': '22:00'}], 5: [{'start': '11:00', 'end': '14:00'}, {'start': '17:00', 'end': '22:00'}], 6: [{'start': '11:00', 'end': '22:00'}], 7: [{'start': '11:00', 'end': '22:00'}]}", 'match_score': 0.619067, 'url': 'https://www.google.com/maps/place/?q=place_id:ChIJ_3Drk2CpQjQRj60tccm_S-c'}, {'place_id': 'ChIJ__nlgOarQjQREEtudHpCT7w', 'name': '豆花、刨冰', 'rating': 4.7, 'num_comments': 10, 'lon': 121.6171295, 'lat': 25.0487693, 'avg_cost': np.nan, 'label_type': '餐廳', 'label': '甜品 餐廳', 'hours': "{1: [{'start': '15:00', 'end': '20:30'}], 2: [{'start': '15:00', 'end': '20:30'}], 3: [{'start': '15:00', 'end': '20:30'}], 4: [{'start': '15:00', 'end': '20:30'}], 5: [{'start': '15:00', 'end': '20:30'}], 6: [{'start': '15:00', 'end': '20:30'}], 7: 'none'}", 'match_score': 0.5325712, 'url': 'https://www.google.com/maps/place/?q=place_id:ChIJ__nlgOarQjQREEtudHpCT7w'}]
    c = [{'星期別': 'none', '時間': 'none', '類別': 'none', '預算': 'none', '出發地點': 'none', '可接受距離門檻(KM)': 'none', '交通方式': 'none'}]
    result = run_test(three,c)
    print(result)