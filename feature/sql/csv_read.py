import ast
import pandas as pd
from .sample_data import load_and_sample_data


def pandas_search(condition_data: dict, detail_info: list[dict]) -> list[dict]:
    '''
    輸入:
        condition_data: dict
            key: 時段名稱(上午/中餐/下午/晚餐/晚上)
            value: 該時段的place_id列表
        detail_info: list[dict]
            使用者的特殊需求，例如 [{'適合兒童': True, '無障礙': False, '內用座位': True}]

    輸出:
        list[dict]: 符合條件的景點資料列表，每個景點包含:
            - place_id: 景點ID
            - name: 景點名稱
            - rating: 評分
            - lon: 經度
            - lat: 緯度
            - label_type: 標籤類型
            - label: 標籤
            - hours: 營業時間
            - period: 時段(morning/lunch/afternoon/dinner/night)
            - url: Google Maps連結
    '''
    # 中文到英文的時段對應
    period_mapping = {
        '上午': 'morning',
        '中餐': 'lunch',
        '下午': 'afternoon',
        '晚餐': 'dinner',
        '晚上': 'night'
    }

    # 處理輸入的中文時段資料，轉換成英文
    condition_records = []
    for zh_period, place_ids in condition_data.items():
        eng_period = period_mapping[zh_period]
        for pid in place_ids:
            condition_records.append({
                'place_id': pid,
                'period': eng_period  # 使用轉換後的英文時段
            })

    # 讀取景點基本資料
    info_df = pd.read_csv('./database/info_df.csv').replace('none', None)

    # 合併基本資料與條件資料
    condition_info_df = pd.merge(
        pd.DataFrame(condition_records),
        info_df,
        on='place_id',
        how='inner'
    )

    # 處理特殊需求條件
    detail_keys = ['內用座位', '洗手間', '適合兒童', '適合團體',
                   '現金', '其他支付', '收費停車', '免費停車', 'wi-fi', '無障礙']
    detail_conditions = {key: detail_info[0].get(key, None)
                         for key in detail_keys}

    # 取得值為True的條件
    true_keys = [key for key, value in detail_conditions.items()
                 if value is True]

    # 根據特殊需求篩選資料
    filtered_df = condition_info_df
    if true_keys:  # 只在有特殊需求時進行篩選
        for key in true_keys:
            filtered_df = filtered_df[
                filtered_df['device_cat'].str.contains(
                    key, na=False, case=False)
            ]

    # 加入營業時間資料
    hours_df = pd.read_csv('./database/hours_df.csv').replace('none', None)
    filtered_df = pd.merge(
        filtered_df,
        hours_df[['place_id', 'hours']],
        on='place_id',
        how='left'
    )

    # 移除無營業時間資料的記錄
    filtered_df = filtered_df[
        filtered_df['hours'].notna() &
        (filtered_df['hours'] != '{}')
    ]

    # 新增 Google Maps 連結
    filtered_df['url'] = ("https://www.google.com/maps/place/?q=place_id:" +
                          filtered_df['place_id'])

    # 依評分排序並取每個時段前25筆
    result = []
    for period in filtered_df['period'].unique():
        period_df = filtered_df[filtered_df['period'] == period]
        top_50 = period_df.nlargest(25, 'rating')[
            ['place_id', 'place_name', 'rating', 'lon', 'lat',
             'label_type', 'label', 'hours', 'period', 'url']
        ]

        # 轉換成字典格式（注意縮排在 for period 迴圈內）
        for _, row in top_50.iterrows():
            try:
                # 處理 hours 字串轉字典
                hours_dict = ast.literal_eval(
                    row['hours']) if isinstance(row['hours'], str) else {}

                # 檢查並修正每一天的營業時間格式
                for day in range(1, 8):
                    if (day not in hours_dict or
                        hours_dict[day] is None or
                        hours_dict[day] == 'none' or
                            hours_dict[day] == [None]):
                        hours_dict[day] = [{'start': '00:00', 'end': '23:59'}]

                result.append({
                    'place_id': row['place_id'],
                    'name': row['place_name'],
                    'rating': float(row['rating']),
                    'lon': float(row['lon']),
                    'lat': float(row['lat']),
                    'label_type': row['label_type'],
                    'label': row['label'],
                    'hours': hours_dict,
                    'period': row['period'],
                    'url': row['url']
                })
            except (ValueError, SyntaxError) as e:
                print(f"轉換營業時間格式失敗 ({row['place_id']}): {e}")
                continue
            except Exception as e:
                print(f"其他錯誤 ({row['place_id']}): {e}")
                continue

    return result


if __name__ == "__main__":
    # 測試用範例資料
    condition_dict = load_and_sample_data('./database/info_df.csv')

    detail_info = [{'無障礙': False}]

    result = pandas_search(condition_dict, detail_info)
    print(f"找到 {len(result)} 個符合條件的景點")
    if result:
        print("第一筆資料範例:")
        print(result[0])
