import pandas as pd
import numpy as np  # 引入 numpy 以生成隨機數

def load_and_sample_data(file_path):
    '''
    隨機產生1句話的place_id
    '''
    # 讀取 info.csv
    data = pd.read_csv(file_path)

    # 隨機選取500筆資料
    random_data = data.sample(n=500, random_state=1)

    # 只保留 place_id 欄位並新增 match_score 欄位
    random_data = random_data[['place_id']]
    random_data['match_score'] = np.random.rand(len(random_data)).round(2)  # 隨機生成介於0到1的數值，並保留兩位小數

    # 將資料轉換為所需的字典格式
    random_dict = {row['place_id']: {"match_score": row['match_score']} for _, row in random_data.iterrows()}
    # print(random_dict)

    return random_dict


# 使用函數
if __name__ == "__main__":
    condition_data = load_and_sample_data(r'C:\Users\Weiii\travel_ROUTER\feature\sql\info_df.csv')
    print(condition_data)
