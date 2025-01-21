import pandas as pd
from feature.plan.utils.check_class import filter_by_label_type
from feature.plan.utils.檢查預算 import filter_by_budget
from feature.plan.utils.檢查距離 import filter_by_distance
from feature.plan.utils.檢查日期 import filter_by_weekday
from feature.plan.utils.檢查時間1 import filter_by_time_without_weekday


def main(points, user_requirements):
    """
    根據使用者需求篩選符合條件的餐廳。
    
    :param points: 資料列表。程
    :param user_requirements: 使用者需求列表。pon
    :return: 符合條件的餐廳 place_id 列表。
    """
    user_filters = user_requirements[0]  

    # 初始化符合條件的餐廳
    matching_place_ids = set(r['place_id'] for r in points)

    # 篩選類別
    desired_label = user_filters.get("類別")
    if desired_label != "none":
        matching_place_ids.intersection_update(filter_by_label_type(points, desired_label))

    # 篩選預算
    user_budget = user_filters.get("預算")
    if user_budget != "none":
        matching_place_ids.intersection_update(filter_by_budget(points, user_budget))

    # 篩選距離
    start_location = user_filters.get("出發地")
    max_distance_km = user_filters.get("可接受距離門檻(KM)")
    if start_location != "none" and max_distance_km != "none":
        matching_place_ids.intersection_update(filter_by_distance(points, start_location, float(max_distance_km)))

    # 篩選星期
    user_weekday = user_filters.get("星期別")
    if user_weekday != "none":
        matching_place_ids.intersection_update(filter_by_weekday(points, user_weekday))

    # 篩選時間
    user_arrival_time = user_filters.get("hours")
    if user_arrival_time != "none":
        matching_place_ids.intersection_update(filter_by_time_without_weekday(points, user_arrival_time))

    return list(matching_place_ids)


if __name__ == "__main__":
    # 測試餐廳數據
    points = [
        {
            'place_id': 1,
            'place_name': '店名1',
            'rating': 4.5,
            'retrival_score': 0.8,
            'comments': 150,
            'lat': 25.0375,
            'lon': 121.5637,
            'new_label_type': '咖啡廳',
            'hours': {
                1: [{'start': '09:00', 'end': '21:00'}],
                2: [{'start': '09:00', 'end': '21:00'}],
                3: 'none',
                4: [{'start': '09:00', 'end': '21:00'}],
                5: [{'start': '09:00', 'end': '21:00'}],
                6: [{'start': '09:00', 'end': '21:00'}],
                7: [{'start': '09:00', 'end': '17:00'}],
            },
            'new_avg_cost': 300,
            'Location_URL': 'https://example.com',
            '圖片URL': 'https://example.com',
        },
        {
            'place_id': 2,
            'place_name': '店名1',
            'rating': 4.5,
            'retrival_score': 0.8,
            'comments': 150,
            'lat': 25.0375,
            'lon': 121.5637,
            'new_label_type': '咖啡廳',
            'hours': {
                1: [{'start': '09:00', 'end': '21:00'}],
                2: [{'start': '09:00', 'end': '21:00'}],
                3: 'none',
                4: [{'start': '09:00', 'end': '21:00'}],
                5: [{'start': '09:00', 'end': '21:00'}],
                6: [{'start': '09:00', 'end': '21:00'}],
                7: [{'start': '09:00', 'end': '17:00'}],
            },
            'new_avg_cost': 300,
            'Location_URL': 'https://example.com',
            '圖片URL': 'https://example.com',
        },
        {
            'place_id': 3,
            'place_name': '店名2',
            'rating': 4.2,
            'retrival_score': 0.7,
            'comments': 120,
            'lat': 25.0402,
            'lon': 121.5657,
            'new_label_type': '餐廳',
            'hours': {
                1: 'none',
                2: [{'start': '10:00', 'end': '20:00'}],
                3: [{'start': '10:00', 'end': '20:00'}],
                4: [{'start': '10:00', 'end': '20:00'}],
                5: [{'start': '10:00', 'end': '20:00'}],
                6: [{'start': '10:00', 'end': '20:00'}],
                7: [{'start': '10:00', 'end': '16:00'}],
            },
            'new_avg_cost': 500,
            'Location_URL': 'https://example.com',
            '圖片URL': 'https://example.com',
        },
    ]

    # 測試使用者需求
    user_requirements = [
        {
            "星期別": 5,
            "hours": "16:00",
            "類別": "咖啡廳",
            "預算": 300,
            "出發地": "none",
            "可接受距離門檻(KM)": "none",
            "交通類別": "步行",
        }
    ]

    # 執行篩選
    results = main(points, user_requirements)

    # 輸出結果
    print("符合條件的餐廳 place_id:", results)
