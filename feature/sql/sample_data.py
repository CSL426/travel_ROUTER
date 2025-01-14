import pandas as pd


def load_and_sample_data(file_path):
    '''
    輸入:
        file_path: CSV檔案路徑

    輸出:
        dict: 
            key: 時段名稱(上午/中餐/下午/晚餐/晚上)
            value: 該時段的place_id列表
    '''
    # 讀取 info.csv
    data = pd.read_csv(file_path)

    # 隨機選取 restaurant 資料
    restaurant_data = data[
        data['data_type'] == 'restaurant'].sample(n=500, random_state=1)
    lunch_df = restaurant_data.sample(n=250, random_state=1)[['place_id']]
    dinner_df = restaurant_data.drop(lunch_df.index)[['place_id']]

    # 隨機選取 attraction 資料
    attraction_data = data[
        data['data_type'] == 'attraction'].sample(n=750, random_state=1)
    morning_df = attraction_data.sample(n=250, random_state=1)[['place_id']]
    afternoon_df = attraction_data.drop(morning_df.index).sample(
        n=250, random_state=1)[['place_id']]
    night_df = attraction_data.drop(morning_df.index).drop(
        afternoon_df.index)[['place_id']]

    # 將每個時段轉換為中文並加入對應的place_id列表
    period_groups = {
        '上午': morning_df['place_id'].tolist(),
        '中餐': lunch_df['place_id'].tolist(),
        '下午': afternoon_df['place_id'].tolist(),
        '晚餐': dinner_df['place_id'].tolist(),
        '晚上': night_df['place_id'].tolist()
    }

    return period_groups


# 使用函數
if __name__ == "__main__":
    condition_data = load_and_sample_data('./database/info_df.csv')
    print(condition_data)
