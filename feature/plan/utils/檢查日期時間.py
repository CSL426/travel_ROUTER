from datetime import datetime

def is_time_in_range(start, end, check_time):
    """檢查指定時間是否在營業時間範圍內"""
    start_time = datetime.strptime(start, '%H:%M').time()
    end_time = datetime.strptime(end, '%H:%M').time()
    check_time = datetime.strptime(check_time, '%H:%M').time()
    return start_time <= check_time <= end_time

def filter_by_operating_time(schedule, weekday, arrival_time):
    """
    根據用戶提供的星期和到達時間篩選餐廳營業信息。
    schedule: 餐廳營業時間表
    weekday: 用戶提供的星期 (1=週一, 2=週二, ..., 7=週日)
    arrival_time: 用戶的到達時間 (格式: 'HH:MM')
    """
    # 檢查該星期是否營業
    if schedule[weekday] == 'none':
        return False  # 該星期不營業

    # 篩選該星期的營業時間段
    operating_hours = schedule[weekday]
    for time_range in operating_hours:
        if is_time_in_range(time_range['start'], time_range['end'], arrival_time):
            return True  # 找到符合的時間段

    return False  # 沒有符合的時間段

def filter_restaurants(restaurants, weekday, arrival_time):
    """
    篩選出在指定時間和星期營業的餐廳。
    restaurants: 餐廳列表，包含 place_id 和 schedule。
    weekday: 用戶提供的星期 (1=週一, 2=週二, ..., 7=週日)。
    arrival_time: 用戶的到達時間 (格式: 'HH:MM')。
    """
    open_restaurants = []
    for restaurant in restaurants:
        place_id = restaurant['place_id']
        schedule = restaurant['schedule']
        if filter_by_operating_time(schedule, weekday, arrival_time):
            open_restaurants.append(place_id)  # 保留營業中的餐廳

    return open_restaurants

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
    user_weekday = 7  # 週日
    user_arrival_time = '16:00'  # 到達時間

    # 篩選結果
    open_restaurants = filter_restaurants(restaurants, user_weekday, user_arrival_time)
    print("營業中的餐廳 place_id:", open_restaurants)


