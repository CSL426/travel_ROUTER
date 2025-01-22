from geopy.distance import geodesic

def calculate_reverse_normalized_distances_no_threshold(points, user_location):
    """
    計算距離的反向標準化分數。
    
    :points: 資料列表，每個地點包含 place_id 和經緯度。
    :param user_location: 使用者出發地 (lat, lon)。
    :return: 包含 place_id 和反向標準化距離分數的列表。
    """
    results = []
    for point in points:
        point_location = (point['lat'], point['lon'])
        # 計算與使用者的距離
        distance = geodesic(user_location, point_location).kilometers
        # 反向標準化分數計算（距離越大分數越低，距離越小分數越高）
        normalized_score = round((1 / (1 + distance)) * 100, 2)  # 反向標準化公式
        results.append({
            "place_id": point['place_id'],
            "distance_km": round(distance, 2),  # 距離保留兩位小數
            "distance_normalized_score": normalized_score  # 分數保留兩位小數
        })
    return results


if __name__ == "__main__":
    # 測試數據
    points = [
        {'place_id': 1, 'lon': 121.5171, 'lat': 25.0478},
        {'place_id': 2, 'lon': 121.5314, 'lat': 25.0645},
        {'place_id': 3, 'lon': 121.5078, 'lat': 25.0339},
        {'place_id': 4, 'lon': 121.5289, 'lat': 25.0356},
        {'place_id': 5, 'lon': 121.4952, 'lat': 25.0213},
        {'place_id': 6, 'lon': 121.5501, 'lat': 25.0483},
        {'place_id': 7, 'lon': 121.5156, 'lat': 25.0612},
        {'place_id': 8, 'lon': 121.5082, 'lat': 25.0653},
        {'place_id': 9, 'lon': 121.5427, 'lat': 25.0296},
        {'place_id': 10, 'lon': 121.5209, 'lat': 25.0501},
        {'place_id': 11, 'lon': 121.4935, 'lat': 25.0462}
    ]

    user_requirements = [
        {
            "星期別": 1,
            "時間": "10:00",
            "類別": "餐廳",
            "預算": 700,
            "出發地": (25.0478, 121.5171),
            "交通類別": "步行"
        }
    ]

    # 使用者輸入
    user_location = user_requirements[0]['出發地']  # 使用者出發地

    # 計算反向標準化距離分數
    results = calculate_reverse_normalized_distances_no_threshold(points, user_location)

    # 輸出結果
    print("反向標準化距離分數:")
    for result in results:
        print(result)
