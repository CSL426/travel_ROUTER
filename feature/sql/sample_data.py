import pandas as pd

def load_and_sample_data(file_path):
    '''
    隨機產生5句話的place_id
    '''
    # 讀取 info.csv
    data = pd.read_csv(file_path)

    # 隨機選取 restaurant 資料
    restaurant_data = data[data['data_type'] == 'restaurant'].sample(n=500, random_state=1)
    lunch_df = restaurant_data.sample(n=250, random_state=1)[['place_id']]
    dinner_df = restaurant_data.drop(lunch_df.index)[['place_id']]

    # 隨機選取 attraction 資料
    attraction_data = data[data['data_type'] == 'attraction'].sample(n=750, random_state=1)
    morning_df = attraction_data.sample(n=250, random_state=1)[['place_id']]
    afternoon_df = attraction_data.drop(morning_df.index).sample(n=250, random_state=1)[['place_id']]
    night_df = attraction_data.drop(morning_df.index).drop(afternoon_df.index)[['place_id']]

    # 將每個 DataFrame 轉換為列表並新增 "period" 欄位
    lunch_df['period'] = 'lunch'
    dinner_df['period'] = 'dinner'
    morning_df['period'] = 'morning'
    afternoon_df['period'] = 'afternoon'
    night_df['period'] = 'night'

    # 合併成一個 condition_df
    condition_df = pd.concat([lunch_df, dinner_df, morning_df, afternoon_df, night_df], ignore_index=True)

    # 將 condition_df 存成 dict 格式
    condition_dict = condition_df.to_dict(orient='records')
    
    return condition_dict

# 使用函數
condition_data = load_and_sample_data('info_df.csv')
