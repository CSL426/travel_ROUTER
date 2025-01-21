from feature.sql_csv.core.data_pipeline.filter_pipeline import filter_pipeline

def plan_system(system_input: list[dict], special_request_list):
    '''
    ```
    Args: 
        system_input : 情境搜索端含分數的向量搜尋結果
        special_request_list : 特殊要求
    return:
        points : 傳給 情境搜尋的資料
    ```

    '''
    placeID_list = list(system_input[0].keys())
    placeID_list = filter_pipeline(
        placeID_list=placeID_list,
        restaurant_view_classify='',
        special_request_list=special_request_list,
    )
    
    
    print(placeID_list)
    return 


if __name__ == '__main__':
    plan_system_input = [{
                            'ChIJqelWmSGnQjQR0oQv0a6ZJ8o':{"分數": 0.5} ,  # 康小玲      ['外帶外送', '其他支付']
                            'ChIJI-NIexYdaDQRfldAuHBbwmY':{"分數": 0.6} ,  # 無名涼麵    ['現金']
                            'ChIJ28UWAQAdaDQRBDGBOwEMJIY':{"分數": 0.7} ,  # 冰品店      ['外帶外送', '內用座位']
                            'ChIJHRHjiIOuQjQRwvkYlwIEcTQ':{"分數": 0.8} ,  # SK-II       ['無障礙', '其他支付']
                        }]
    special_request_list = [{ '現金': True,}]
    
    plan_system(system_input=plan_system_input, 
                special_request_list=special_request_list)





