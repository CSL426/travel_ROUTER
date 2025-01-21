from datetime import datetime

def is_time_in_range(start, end, target):
    """
    檢查目標時間是否在指定的時間範圍內。 
    ask: 會有的問題是我想找16:00有營業的店同一間店可能會有5天都有營業
    
    start: 時間範圍的起始 (格式: 'HH:MM')。
    end: 時間範圍的結束 (格式: 'HH:MM')。
    target: 用戶抵達時間 (格式: 'HH:MM')。
    :return: True 如果目標時間在範圍內，否則 False。
    """
    target_time = datetime.strptime(target, '%H:%M')
    start_time = datetime.strptime(start, '%H:%M')
    end_time = datetime.strptime(end, '%H:%M')
    return start_time <= target_time <= end_time


def filter_by_time_without_weekday(restaurants, arrival_time):
    """
    根據到達時間篩選營業中的餐廳，忽略星期篩選。
    
    :param restaurants: 餐廳列表，包含 place_id 和 schedule。
    :param arrival_time: 使用者的到達時間 (格式: 'HH:MM')。
    :return: 符合條件的 place_id 列表。
    """
    open_at_time = []
    for restaurant in restaurants:
        schedule = restaurant.get("schedule", {})
        # 遍歷 schedule 中所有的營業時間
        for weekday, time_ranges in schedule.items():
            if time_ranges == 'none':  # 當日無營業時間，跳過
                continue
            # 檢查該日期的每個時間段
            for time_range in time_ranges:
                if is_time_in_range(time_range['start'], time_range['end'], arrival_time):
                    open_at_time.append(restaurant['place_id'])
                    break  # 已找到符合條件的時間段，跳出時間段迴圈
    return open_at_time


if __name__ == "__main__":
    # 測試數據
    restaurants = [
        {
            "place_id": 1,
            "schedule": {
                1: 'none',
                2: [{'start': '09:00', 'end': '21:00'}],
                3: [{'start': '09:00', 'end': '21:00'}],
                4: [{'start': '09:00', 'end': '21:00'}],
                5: [{'start': '09:00', 'end': '21:00'}],
                6: [{'start': '09:00', 'end': '21:00'}],
                7: [{'start': '09:00', 'end': '17:00'}]
            }
        },
        {
            "place_id": 2,
            "schedule": {
                1: 'none',
                2: [{'start': '10:00', 'end': '20:00'}],
                3: [{'start': '10:00', 'end': '20:00'}],
                4: [{'start': '10:00', 'end': '20:00'}],
                5: [{'start': '10:00', 'end': '20:00'}],
                6: [{'start': '10:00', 'end': '20:00'}],
                7: [{'start': '10:00', 'end': '16:00'}]
            }
        },
        {
            "place_id": 3,
            "schedule": {
                1: 'none',
                2: 'none',
                3: 'none',
                4: [{'start': '12:00', 'end': '18:00'}],
                5: [{'start': '12:00', 'end': '18:00'}],
                6: [{'start': '12:00', 'end': '18:00'}],
                7: [{'start': '12:00', 'end': '18:00'}]
            }
        }
    ]

    # 使用者輸入
    user_arrival_time = '16:00'  # 到達時間

    # 篩選符合條件的餐廳
    open_restaurants = filter_by_time_without_weekday(restaurants, user_arrival_time)
    place_id = open_restaurants

    # 輸出結果
    print("符合 16:00 營業的餐廳 place_id:", place_id)

