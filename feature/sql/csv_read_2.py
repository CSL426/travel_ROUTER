# 從向量搜尋跟llm那邊獲得資訊並讀取csv調度出資料(最符合的前100)
import pandas as pd
from sample_data_2 import load_and_sample_data

def pandas_search(condition_data: list[dict], detail_info: list[dict]) -> list[dict]:
    '''
    結合向量資料搜尋出來的place_id與使用者提出的特殊需求，產出符合的結構資料
    '''
    # 步驟1: 將 condition_data 轉換為 DataFrame
    condition_df = pd.DataFrame.from_records(
        [(place_id, data['match_score']) for place_id, data in condition_data.items()],
        columns=['place_id', 'match_score']
    )

    # 讀取 info_df 並與 condition_data 交集形成 condition_info_df
    info_df = pd.read_csv('info_df.csv')
    condition_info_df = pd.merge(condition_df, info_df, on='place_id', how='inner')
    # print("condition_info_df如下")
    # print(condition_info_df)

    # 步驟2: 轉換 detail_info 的 key:value
    detail_keys = ['內用座位', '洗手間', '適合兒童', '適合團體', '現金', '其他支付', '收費停車', '免費停車', 'wi-fi', '無障礙']
    detail_conditions = {key: detail_info[0].get(key, None) for key in detail_keys}
    # print("detail_conditions如下")
    # print(detail_conditions)
    
    # 合併 detail_conditions 中值為 True 的鍵為一個列表
    true_keys = [key for key, value in detail_conditions.items() if value is True]
    # print("true_keys如下")
    # print(true_keys)  # 打印值為 True 的鍵列表

    # 步驟3: 從 condition_info_df 中篩選符合 true_keys 的資料
    filtered_df = condition_info_df
    for key in true_keys:
        filtered_df = filtered_df[filtered_df['device_cat'].str.contains(key, na=False, case=False)]  # 忽略大小寫

    # 確保 device_cat 同時包含所有 true_keys 的元素
    filtered_df = filtered_df[filtered_df['device_cat'].apply(lambda x: all(k in x for k in true_keys))]
    # print("filtered_df如下")
    # print(filtered_df)  # 打印當前篩選後的資料

    # 讀取 hours_df.csv 並根據 place_id 加入 hours 欄位於 filtered_df
    hours_df = pd.read_csv('hours_df.csv')  # 讀取 hours_df.csv
    filtered_df = pd.merge(filtered_df, hours_df[['place_id', 'hours']], on='place_id', how='left')  # 根據 place_id 合併

    # 移除 hours 欄位為空值或為 '{}' 的資料
    filtered_df = filtered_df[filtered_df['hours'].notna() & (filtered_df['hours'] != '{}')]  # 移除 hours 為空值或為 '{}' 的資料

    # 新增url欄位
    filtered_df['url'] = "https://www.google.com/maps/place/?q=place_id:" + filtered_df['place_id']  # 新增 url 欄位
    
    # 步驟4: 依 rating 高到低，直接返回所有資料
    result = []

    # 直接獲取所有資料，並依 rating 進行排序
    top_tier = filtered_df.nlargest(len(filtered_df), 'rating')[['place_id', 'place_name', 'rating', 'comments', 'lon', 'lat', 'avg_cost', 'label_type', 'label', 'hours', 'match_score', 'url']]
    
    for _, row in top_tier.iterrows():
        result.append({
                'place_id': row['place_id'],  # 修改為 'placeID'
                'name': row['place_name'],
                'rating': row['rating'],
                'num_comments': row['comments'],
                'lon': row['lon'],
                'lat': row['lat'],
                'avg_cost': row['avg_cost'],
                'label_type': row['label_type'],
                'label': row['label'],
                'hours': row['hours'],
                'match_score': row['match_score'],
                'url': row['url']
        })

    # 將結果寫入 output.txt
    with open('output_2.txt', 'w', encoding='utf-8') as f:
        for record in result:
            f.write(f"{record}\n")  # 將每個記錄寫入檔案

    return result  # 返回格式化後的結果

if __name__ == "__main__":
    # 使用 load_and_sample_data 函數獲取 condition_dict
    condition_dict = load_and_sample_data('info_df.csv')

    # 假設 detail_info 是從某個地方獲取的資料
    detail_info = [{'適合兒童': True, '無障礙': False, '內用座位': True}]  # 示例資料

    # 執行 pandas_search 並打印結果
    result = pandas_search(condition_dict, detail_info)
    # print("result如下")
    # print(result[1])  # 打印執行結果
