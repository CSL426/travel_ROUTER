def special_request(    
                    placeID_list, 
                    request_list: list[dict],
                    ETL_dataframe, 
                    ): 
    '''
    根據 request_list 篩選符合條件的選項
    
    ```
    Args:
        placeID_list (list): 包含 placeID 的列表 ['placeID1', 'placeID2', ....]
        request_list (list[dict]): 篩選要求
        ETL_dataframe : ETL_df 表 
    
    Returns:
        list: 篩選後的 placeID 列表。
    ```
    '''



    return ['device_cat']



if __name__ == '__main__':
    from feature.sql_v2.utils.ETL_dataframe_generate import ETL_dataframe_generate
    placeID_list = [
                    'ChIJqelWmSGnQjQR0oQv0a6ZJ8o',    # 康小玲 線上書店交易平台 online bookstores
                    'ChIJI-NIexYdaDQRfldAuHBbwmY',    # 無名涼麵/雙醬涼麵/現場營業時間下午4~9點/線上營業時間24小時
                    'ChIJ28UWAQAdaDQRBDGBOwEMJIY',    # 冰品店
                    'ChIJHRHjiIOuQjQRwvkYlwIEcTQ',    # SK-II大葉高島屋專櫃
                    ]
    ETL_dataframe = ETL_dataframe_generate()

    request_list = [{'內用座位': True, '洗手間': False, '適合兒童': False, '適合團體': False, '現金': False,
          '其他支付': False, '收費停車': False, '免費停車': False, 'wi-fi': False, '無障礙': False}]
    
    placeID_list = special_request(
                        placeID_list=placeID_list,
                        request_list=request_list,
                        ETL_dataframe=ETL_dataframe,
                    )
    

    
    print(placeID_list)