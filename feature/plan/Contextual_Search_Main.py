from feature.plan.utils.Filter_Criteria.check_class import filter_by_label_type
from feature.plan.utils.Filter_Criteria.check_budget import filter_by_budget
from feature.plan.utils.Filter_Criteria.check_distance import filter_by_distance
from feature.plan.utils.Filter_Criteria.check_date import filter_by_weekday
from feature.plan.utils.Filter_Criteria.check_time import filter_by_time_without_weekday
from feature.plan.utils.Norma_lization.similarity_score_normalized import normalize_similarity
from feature.plan.utils.Norma_lization.comment_score_normalized import normalize_and_match, load_extracted_data
from feature.plan.utils.Norma_lization.distances_score_normalized import calculate_reverse_normalized_distances_no_threshold


def main(points, user_requirements):
    """
    根據使用者需求篩選符合條件的餐廳。
    
    :param points: 資料列表。
    :param user_requirements: 使用者需求列表。
    :return: 符合條件的餐廳 place_id 列表。
    """
    user_filters = user_requirements[0]
    matching_place_ids = set(r['place_id'] for r in points)

    # 篩選條件
    desired_label = user_filters.get("類別")
    if desired_label != "none":
        matching_place_ids.intersection_update(filter_by_label_type(points, desired_label))

    user_budget = user_filters.get("預算")
    if user_budget != "none":
        matching_place_ids.intersection_update(filter_by_budget(points, user_budget))

    start_location = user_filters.get("出發地", "none")
    max_distance_km = user_filters.get("可接受距離門檻(KM)", "none")
    if max_distance_km == "none":
        max_distance_km = 10
    else:
        max_distance_km = float(max_distance_km)
    if start_location == "none":
        start_location = (25.0418, 121.5654)
    else:
        start_location = tuple(map(float, start_location.split(',')))
    matching_place_ids.intersection_update(filter_by_distance(points, start_location, max_distance_km))

    user_weekday = user_filters.get("星期別")
    if user_weekday != "none":
        matching_place_ids.intersection_update(filter_by_weekday(points, user_weekday))

    user_arrival_time = user_filters.get("hours")
    if user_arrival_time != "none":
        matching_place_ids.intersection_update(filter_by_time_without_weekday(points, user_arrival_time))

    return list(matching_place_ids)


def calculate_weighted_scores(points, user_location, weights):
    """
    計算每個地點的加權總分，並僅返回指定欄位。
    
    :param points: 地點資料列表。
    :param user_location: 使用者出發地 (lat, lon)。
    :param weights: 權重字典，包含距離、評論分數、相似性。
    :return: 排序後的前 10 地點列表（僅包含指定欄位）。
    """
    points = normalize_similarity(points)
    emotion_analysis_path = r"./data/emotion_analysis.csv"
    extracted_data = load_extracted_data(emotion_analysis_path)
    points = normalize_and_match(points, extracted_data).to_dict(orient="records")

    distance_scores = calculate_reverse_normalized_distances_no_threshold(points, user_location)
    distance_map = {d['place_id']: d['distance_normalized_score'] for d in distance_scores}
    for point in points:
        point['distance_normalized_score'] = distance_map.get(point['place_id'], 0)

    for point in points:
        point['weighted_score'] = (
            weights['distance'] * point.get('distance_normalized_score', 0) +
            weights['comments'] * point.get('comment_score_normalized', 0) +
            weights['similarity'] * point.get('retrival_Normalization', 0)
        )

    points.sort(key=lambda x: x['weighted_score'], reverse=True)
    
    # 過濾需要的欄位
    required_fields = {'place_id', 'place_name', 'rating', 'lat', 'lon', 'new_avg_cost', 'hours', 'Location_URL', 'image_url'}
    filtered_points = [
        {k: v for k, v in point.items() if k in required_fields}
        for point in points[:10]
    ]
    
    return filtered_points



if __name__ == "__main__":
    from pprint import pprint

    # 測試數據
    points = [
        {
            'place_id': 'ChIJ-aSxVAAdaDQR69yHKL4i-jc',
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
            'image_url': 'https://example.com',
        },
        {
            'place_id': 'ChIJ-8OvfTepQjQR6_LN00q5_IY',
            'place_name': '店名2',
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
            'image_url': 'https://example.com',
        },
        {
            'place_id': 'ChIJ-2qAiBJTXTQRFT23-FNNQwg',
            'place_name': '店名3',
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
            'image_url': 'https://example.com',
        },
                {
            'place_id': 'ChIJ-0ecHZqrQjQRXtoq3UKkPaM',
            'place_name': '店名4',
            'rating': 4.2,
            'retrival_score': 0.7,
            'comments': 120,
            'lat': 25.0402,
            'lon': 121.5657,
            'new_label_type': '餐廳',
            'hours': {
                1: [{'start': '10:00', 'end': '20:00'}],
                2: [{'start': '10:00', 'end': '20:00'}],
                3: [{'start': '10:00', 'end': '20:00'}],
                4: [{'start': '10:00', 'end': '20:00'}],
                5: [{'start': '10:00', 'end': '20:00'}],
                6: [{'start': '10:00', 'end': '20:00'}],
                7: [{'start': '10:00', 'end': '16:00'}],
            },
            'new_avg_cost': 500,
            'Location_URL': 'https://example.com',
            'image_url': 'https://example.com',
        },
    ]

    # 測試使用者需求
    user_requirements = [
        {
            "星期別": 1,
            "hours": "16:00",
            "類別": "none",
            "預算": 400,
            "出發地": "none",
            "可接受距離門檻(KM)": "none",
            "交通類別": "步行",
        }
    ]
    weights = {'distance': 0.2, 'comments': 0.4, 'similarity': 0.4}

    filtered_place_ids = main(points, user_requirements)
    filtered_points = [point for point in points if point['place_id'] in filtered_place_ids]
    sorted_results = calculate_weighted_scores(filtered_points, (25.0375, 121.5637), weights)

    print("排序結果:")
    for result in sorted_results:
        pprint(result, sort_dicts=False)
    
