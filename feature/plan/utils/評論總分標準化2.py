import pandas as pd

def load_extracted_data(emotion_analysis_path):
    """
    從 CSV 文件中提取 place_id 和 總體評價。
    
    :param file_path: CSV 文件的路徑。
    :return: 提取的數據列表 (List[Dict])。
    """
    # 加載 CSV 文件
    data = pd.read_csv(emotion_analysis_path)

    # 提取 place_id 和 總體評價
    extracted_data = data[["place_id", "總體評價"]].to_dict(orient="records")
    return extracted_data



def normalize_and_match(restaurants, extracted_data):
    """
    僅將 restaurants 中的 place_id 參與標準化，並匹配結果。
    
    :param restaurants: List[Dict]，包含 place_id 的餐廳列表。
    :param extracted_data: List[Dict]，包含 place_id 和 總體評價 的數據。
    :return: DataFrame，包含匹配結果和標準化評價。
    """
    # 將 extracted_data 轉為 DataFrame
    extracted_df = pd.DataFrame(extracted_data)

    # 將 restaurants 轉為 DataFrame
    restaurants_df = pd.DataFrame(restaurants)

    # 只保留 restaurants 中有的 place_id
    place_ids_in_restaurants = restaurants_df["place_id"].unique()
    filtered_extracted_df = extracted_df[extracted_df["place_id"].isin(place_ids_in_restaurants)]

    # 對 "總體評價" 欄位進行標準化
    if "總體評價" in filtered_extracted_df.columns:
        filtered_extracted_df["comment_score_normalized"] = (
            (filtered_extracted_df["總體評價"] - filtered_extracted_df["總體評價"].min()) /
            (filtered_extracted_df["總體評價"].max() - filtered_extracted_df["總體評價"].min())
        )*100
    
    # 四捨五入到小數點後兩位
        filtered_extracted_df["comment_score_normalized"] = filtered_extracted_df["comment_score_normalized"].round(2)

    # 合併兩個 DataFrame，根據 place_id 匹配
    merged_df = pd.merge(restaurants_df, filtered_extracted_df, on="place_id", how="left")

    return merged_df


if __name__ == "__main__":
    # 文件路徑
    emotion_analysis_path = r"./data/emotion_analysis.csv"

    # 從文件中提取數據
    extracted_data = load_extracted_data(emotion_analysis_path)

    # 測試數據
    restaurants = [
        {'place_id': 'ChIJ---TJYypQjQRNipOm6saF74'}, #7.50
        {'place_id': 'ChIJ---TJYypQjQRNipOm6saF74'}, #7.50 
        {'place_id': 'ChIJ--FASY2sQjQR-zzjANSErLk'}, #4.50
        {'place_id': 'ChIJ--IAVHCpQjQREro-d5JTYxU'}, #5.00
        {'place_id': 'ChIJ--tcLdWvQjQR-nAfNjIShK0'}, #7.33
        {'place_id': 'ChIJ-0ecHZqrQjQRXtoq3UKkPaM'}, #9.00
        {'place_id': 'ChIJ-0LBJE2vQjQR_J6RcfMmWNo'}, #7.50
        {'place_id': 'ChIJ-2J0amatQjQREtiVMjZoflE'}, #8.83
        {'place_id': 'ChIJ-2qAiBJTXTQRFT23-FNNQwg'}, #7.67
        {'place_id': 'ChIJ-5rqdqepQjQRfOxQQJFWA2U'}, #7.67
        {'place_id': 'ChIJ-6uVfm4CaDQRAlb_HRO87DA'}, #3.00 
        {'place_id': 'ChIJ-8OvfTepQjQR6_LN00q5_IY'}, #9.00
        {'place_id': 'ChIJ-aSxVAAdaDQR69yHKL4i-jc'}, #8.00
    ]

    # 執行標準化並匹配
    result_df = normalize_and_match(restaurants,extracted_data)

    # 打印結果
    print("合併並標準化的結果:")
    print(result_df)
