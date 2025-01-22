def normalize_similarity(points):
    """
    對相似性分數進行標準化。
    
    :points: 資料列表，每個地點包含 place_id 和 相似性。
    被篩選出的那一包
    :return: 包含標準化相似性的資料列表。
    """
    # 提取所有相似性分數
    similarities = [p['retrival_score'] for p in points]

    # 計算最小值和最大值
    min_similarity = min(similarities)
    max_similarity = max(similarities)

    # 標準化計算
    for point in points:
        original_score = point['retrival_score']
        normalized_score = ((original_score - min_similarity) / (max_similarity - min_similarity)) * 100
        point['retrival_Normalization'] = round(normalized_score, 2)  # 保留兩位小數
    return points


if __name__ == "__main__":
    # 原始資料
    points = [
        {'place_id': 1, 'retrival_score': 0.83},
        {'place_id': 2, 'retrival_score': 0.91},
        {'place_id': 3, 'retrival_score': 0.75},
        {'place_id': 4, 'retrival_score': 0.68},
        {'place_id': 5, 'retrival_score': 0.94},
        {'place_id': 6, 'retrival_score': 0.88},
        {'place_id': 7, 'retrival_score': 0.73},
        {'place_id': 8, 'retrival_score': 0.95},
        {'place_id': 9, 'retrival_score': 0.61},
        {'place_id': 10, 'retrival_score': 0.79}
    ]

    # 標準化處理
    normalized_points = normalize_similarity(points)

    # 輸出結果
    print("標準化後的相似性分數:")
    for point in normalized_points:
        print(point)
