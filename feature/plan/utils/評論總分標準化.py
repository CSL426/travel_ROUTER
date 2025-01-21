import pandas as pd

# CSV 文件路径
emotion_analysis_path = r"./data/emotion_analysis.csv"

# 加载文件
data = pd.read_csv(emotion_analysis_path)

# 提取 place_id 和 總體評價
extracted_data = data[["place_id", "總體評價"]].to_dict(orient="records")

# # 檢查前 10 项
# print(extracted_data[:10])

def normalize_and_match(restaurants, extracted_data):
    """
    將 extracted_data 的評分進行標準化，並與 restaurants 進行匹配。
    
    :param restaurants: List[Dict]，包含 place_id 的餐廳列表。
    :param extracted_data: List[Dict]，包含 place_id 和評分的數據。
    :return: DataFrame，包含匹配結果和標準化評價。
    """
    # 將 extracted_data 轉為 DataFrame
    extracted_df = pd.DataFrame(extracted_data)

    # 將 "評分" 欄位進行標準化
    if "評分" in extracted_df.columns:
        extracted_df["標準化評分"] = (extracted_df["評分"] - extracted_df["評分"].min()) / (
            extracted_df["評分"].max() - extracted_df["評分"].min()
        )

    # 將 restaurants 轉為 DataFrame
    restaurants_df = pd.DataFrame(restaurants)

    # 合併兩個 DataFrame，根據 place_id 匹配
    merged_df = pd.merge(restaurants_df, extracted_df, on="place_id", how="left")

    return merged_df


if __name__ == "__main__":
    # 測試數據
    restaurants = [
        {'place_id': 'ChIJ---TJYypQjQRNipOm6saF74'},
        {'place_id': 'ChIJ---TJYypQjQRNipOm6saF74'},
        {'place_id': 'ChIJ--FASY2sQjQR-zzjANSErLk'},
        {'place_id': 'ChIJ--IAVHCpQjQREro-d5JTYxU'},
        {'place_id': 'ChIJ--tcLdWvQjQR-nAfNjIShK0'}
    ]
    extracted_data = [
        {'place_id': 'ChIJ---TJYypQjQRNipOm6saF74', '評分': 7.5},
        {'place_id': 'ChIJ--a3zLelQjQRVYdmUEq4SVM', '評分': 7.5},
        {'place_id': 'ChIJ--BGGROqQjQRcOamjS8UMW4', '評分': 5.33},
        {'place_id': 'ChIJ--FASY2sQjQR-zzjANSErLk', '評分': 4.5},
        {'place_id': 'ChIJ--IAVHCpQjQREro-d5JTYxU', '評分': 5.0},
        {'place_id': 'ChIJ--MkGuilQjQRDCEmUAncjwM', '評分': 7.5},
        {'place_id': 'ChIJ--OtBC2qQjQRsSZzy2NIUbc', '評分': 7.5},
        {'place_id': 'ChIJ--tcLdWvQjQR-nAfNjIShK0', '評分': 7.33},
        {'place_id': 'ChIJ-0C6XhKpQjQRcNsw9_B7Zqw', '評分': 8.67},
        {'place_id': 'ChIJ-0Ccg8oCaDQRNywXfRc11vc', '評分': 2.0}
    ]
    # 調用函數
    result_df = normalize_and_match(restaurants, extracted_data)

    # 打印結果
    print("合併並標準化的結果:")
    print(result_df)
