import pandas as pd

def load_extracted_data(file_path):
    """
    從 CSV 文件中提取 place_id 和 總體評價。
    
    :param file_path: CSV 文件的路徑。
    :return: 提取的數據列表 (List[Dict])。
    """
    # 加載 CSV 文件
    data = pd.read_csv(file_path)

    # 提取 place_id 和 總體評價
    extracted_data = data[["place_id", "總體評價"]].to_dict(orient="records")
    return extracted_data


def normalize_and_match(restaurants, extracted_data):
    """
    將 extracted_data 的評分進行標準化，並與 restaurants 進行匹配。
    
    :param restaurants: List[Dict]，包含 place_id 的餐廳列表。
    :param extracted_data: List[Dict]，包含 place_id 和 總體評價 的數據。
    :return: DataFrame，包含匹配結果和標準化評價。
    """
    # 將 extracted_data 轉為 DataFrame
    extracted_df = pd.DataFrame(extracted_data)

    # 將 "總體評價" 欄位進行標準化
    if "總體評價" in extracted_df.columns:
        extracted_df["標準化評分"] = (extracted_df["總體評價"] - extracted_df["總體評價"].min()) / (
            extracted_df["總體評價"].max() - extracted_df["總體評價"].min()
        )

    # 將 restaurants 轉為 DataFrame
    restaurants_df = pd.DataFrame(restaurants)

    # 合併兩個 DataFrame，根據 place_id 匹配
    merged_df = pd.merge(restaurants_df, extracted_df, on="place_id", how="left")

    return merged_df


if __name__ == "__main__":
    # 文件路徑
    emotion_analysis_path = r"./data/emotion_analysis.csv"

    # 從文件中提取數據
    extracted_data = load_extracted_data(emotion_analysis_path)

    # 測試數據
    restaurants = [
        {'place_id': 'ChIJ---TJYypQjQRNipOm6saF74'},
        {'place_id': 'ChIJ---TJYypQjQRNipOm6saF74'},
        {'place_id': 'ChIJ--FASY2sQjQR-zzjANSErLk'},
        {'place_id': 'ChIJ--IAVHCpQjQREro-d5JTYxU'},
        {'place_id': 'ChIJ--tcLdWvQjQR-nAfNjIShK0'}
    ]

    # 執行標準化並匹配
    result_df = normalize_and_match(restaurants, extracted_data)

    # 打印結果
    print("合併並標準化的結果:")
    print(result_df)
