import sys
import os

# 添加專案根目錄到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import random
import pandas as pd
from geopy.distance import geodesic
import math
import json
from feature.sql import csv_read_2, sample_data_2

def run_test(user_demand, require_info):  # Modified to accept two parameters
    # 讀取資料
    def load_data():
        condition_data = sample_data_2.load_and_sample_data(r'C:\Users\Weiii\travel_ROUTER\feature\sql\info_df.csv')
        detail_info = [{'適合兒童': True, '無障礙': False, '內用座位': True}]  # 示例特殊需求
        return csv_read_2.pandas_search(condition_data, detail_info)

    # 根據 user_demand 和 require_info 篩選符合條件的餐廳
    def filter_results_by_demand(results, user_demand, require_info):  # Modified to accept require_info
        filtered_results = []
        condition_hours = pd.read_csv(r'C:\Users\Weiii\travel_ROUTER\feature\plan\transformed_df.csv')

        for condition in results:
            print(f"檢查餐廳: {condition.get('name', '未知')}")

            place_id = condition.get('place_id')
            hours_data = condition_hours[condition_hours['place_id'] == place_id]

            if hours_data.empty:
                print(f"跳過 {condition.get('name', '未知')}，未找到營業時間資料")
                continue

            restaurant_coords = (condition.get('lat', None), condition.get('lon', None))
            if None in restaurant_coords or restaurant_coords == (0, 0):
                print(f"跳過 {condition.get('name', '未知')} 經緯度缺失")
                continue

            distance = geodesic(user_demand['出發地'], restaurant_coords).kilometers
            condition['distance'] = distance

            try:
                user_time = int(str(user_demand['時間']).split(":")[0]) if isinstance(user_demand['時間'],str) else user_demand['時間']
            except (ValueError, AttributeError):
                print(f"跳過 {condition.get('name', '未知')} 時間格式不正確")
                continue

            week_matches = hours_data[hours_data['weekday'] == user_demand['星期別']]
            if week_matches.empty:
                print(f"跳過 {condition.get('name', '未知')} 星期別不符合")
                continue
            week_matches = week_matches[week_matches['start_time'] != 'none']
            week_matches = week_matches[week_matches['end_time'] != 'none']

            week_matches['start_time'] = week_matches['start_time'].astype(str).str.split(':').str[0].astype(int)
            week_matches['end_time'] = week_matches['end_time'].astype(str).str.split(':').str[0].astype(int)
            
            time_matches = week_matches[
                (week_matches['start_time'] <= user_time) &
                (week_matches['end_time'] >= user_time)
            ]
            if time_matches.empty:
                print(f"跳過 {condition.get('name', '未知')} 時間不符合")
                continue

            if condition.get('label_type') != user_demand['類別']:
                print(f"跳過 {condition.get('name', '未知')} 類別不符合")
                continue

            avg_cost = condition.get('avg_cost', float('inf'))
            if pd.isna(avg_cost) or not (user_demand['預算'] - 100 <= avg_cost <= user_demand['預算'] + 100):
                print(f"跳過 {condition.get('name', '未知')} 預算超出")
                continue

            if not (user_demand['可接受距離(KM)'] - 20 <= distance <= user_demand['可接受距離(KM)'] + 20):
                print(f"跳過 {condition.get('name', '未知')} 距離超出")
                continue

            # Add additional filtering based on require_info if needed
            # ...

            filtered_results.append(condition)
        return filtered_results

    # 權重
    weights = {
        "price": 0.4,
        "distance": 0.3,
        "rating": 0.2,
        "match": 0.1
    }

    # 計算分數
    def calculate_scores(results):
        if not results:
            return []

        distances = [condition['distance'] for condition in results]
        min_distance = min(distances) if distances else 0
        max_distance = max(distances) if distances else 0

        prices = [c.get('avg_cost', 0) for c in results if c.get('avg_cost', 0) > 0]
        min_price = min(prices) if prices else 0
        max_price = max(prices) if prices else 1

        max_reviews = max([c.get('num_comments', 0) for c in results]) if results else 1

        for condition in results:
            price = condition.get('avg_cost', None)
            condition['price_score'] = 10 * (1 - (price - min_price) / (max_price - min_price)) if price is not None and max_price > min_price else 10 if price is not None else 0

            distance = condition['distance']
            condition['distance_score'] = 10 * (1 - (distance - min_distance) / (max_distance - min_distance)) if max_distance > min_distance else 10

            rating = condition.get('rating', 0)
            reviews = condition.get('num_comments', 0)
            condition['rating_score'] = (
                (rating * 2) + (math.log(reviews + 1) / math.log(max_reviews + 1) * 5)
            ) if rating > 0 and reviews > 0 else 0

            match = condition.get('match_score', 0)
            condition['match_score'] = match * 10 if match else 0
        return results

    # 計算總分
    def calculate_total_score(results):
        for condition in results:
            condition["total_score"] = (
                condition.get("price_score", 0) * weights["price"] +
                condition.get("distance_score", 0) * weights["distance"] +
                condition.get("rating_score", 0) * weights["rating"] +
                condition.get("match_score", 0) * weights["match"]
            )
        return results

    # 執行流程
    data = load_data()
    results = data

    filtered_results = filter_results_by_demand(results, user_demand, require_info)  # Modified to pass require_info
    scored_results = calculate_scores(filtered_results)
    final_results = calculate_total_score(scored_results)

    sorted_results = sorted(final_results, key=lambda x: x.get('total_score',0), reverse=True)[:15]

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

    with open('test.txt', 'w', encoding='utf-8-sig') as f:
        for condition in output_list:
            f.write(f"{condition['name']}: {condition}\n")

    print("篩選結果已輸出至 test.txt。")
    print("推薦如下：")
    for condition in output_list:
        print(f"{condition['name']}: 總分 {condition['total_score']}")

    return output_list

# 執行測試函數
if __name__ == "__main__":
    # 直接帶入 user_demand
    user_demand = {
        '星期別': 5,
        '時間': '12:00',
        '類別': '餐廳',
        '預算': 300,
        '出發地': (24.79824463059828, 121.58730583548193),
        '可接受距離(KM)': 9,
        '交通類別': '開車'
    }

    require_info = {
        # Add any required info parameters here
    }

    # 使用 load_and_sample_data 函數獲取 condition_dict
    condition_dict = sample_data_2.load_and_sample_data(r'C:\Users\Weiii\travel_ROUTER\feature\sql\info_df.csv')

    # 執行 pandas_search
    result = csv_read_2.pandas_search(condition_dict, [user_demand])
    print("result如下")
    print(result[1])

    sorted_results = run_test(user_demand, require_info)  # Modified to pass both parameters