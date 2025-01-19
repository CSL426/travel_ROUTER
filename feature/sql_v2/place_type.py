import pandas as pd
import vector_search as vector_search
import spec_demand

def type_filter(condition_data: dict, detail_info: list[dict]) -> list:

    """
    將特殊需求條件的filter_list，檢視輸出需求為餐廳or景點後篩選出符合label_type的type_list
    """

    id_list = vector_search.merge_id(condition_data)
    id_list = spec_demand.demand_filter(condition_data, detail_info)
    id_list = pd.DataFrame(id_list, columns=['place_id'])

    # keys in condition_data
    keys = condition_data.keys()
    
    # read ETL_df.csv and merge with id_list
    ETL_df = pd.read_csv(r'data\ETL_df.csv', usecols=['place_id', 'new_label_type'])
    ETL_df = pd.merge(ETL_df, id_list, on='place_id', how='inner')

    # filter data from ETL_df
    if '中餐' in keys or '晚餐' in keys:
        filtered_df = ETL_df[ETL_df['new_label_type'].isin(['咖啡廳', '小吃', '餐廳'])]
    else:
        filtered_df = ETL_df[~ETL_df['new_label_type'].isin(['咖啡廳', '小吃', '餐廳'])]

    type_list = filtered_df['place_id'].tolist()

    return type_list

if __name__ == "__main__":
    
    # trip
    condition_data = {
         '上午' : ['ChIJqelWmSGnQjQR0oQv0a6ZJ8o','ChIJI-NIexYdaDQRfldAuHBbwmY','ChIJ28UWAQAdaDQRBDGBOwEMJIY','ChIJHRHjiIOuQjQRwvkYlwIEcTQ','ChIJbVVGbyMdaDQRA4fwQM5a8Zo','ChIJJRIAm9CrQjQRVQMRfuCQIz8','ChIJJSMu6lauQjQRBVTCVxC25nU','ChIJvw3uhB-vQjQRmoAxj_eGZ6w',],
         '中餐' : ['ChIJzZsyrjaqQjQR9FND-RCuqXk','ChIJbR_veWKrQjQRyNk7HMd4VQQ','ChIJ56tavM-rQjQRpb_MPrkhHGQ','ChIJOSS68pquQjQRkjoarVAbQy8','ChIJtyX0fOapQjQRE-YyACXj1n4','ChIJBTFKTW9VXTQRYZ16hHDThow','ChIJ96mJRw-nQjQRvuEBDkiJ9Ns','ChIJAdiX-eEdaDQR0yp_crBU3lA',],
         '下午' : ['ChIJiz146XipQjQRPVUgvrZhIzI','ChIJQV-ginuvQjQRduARdLPHkQI','ChIJd46wSeADaDQRSAxunpx2RqI','ChIJnRQY8tUcaDQRiOI4CIQq6WM','ChIJWeThTAADaDQRCOTCy0na-ko','ChIJrbj1LIGsQjQRtl609U2spdk','ChIJszfi8aVVXTQRp8CmDFdK43A','ChIJOwf8sTypQjQR4UYi7n8NoaM',],
         '晚餐' : ['ChIJg5D8feOrQjQRQ4RKqUbpdUM','ChIJdzQVQo-pQjQRD1hZB7p9tFA','ChIJzeV8oKSuQjQR8vW2lapRpio','ChIJ-VQi78KpQjQRuem8YnBUX4c','ChIJz4fiL6WuQjQR6y15lAOjeRY','ChIJkWFgHQMCaDQRNXr5N6bL7OQ','ChIJ23IFu9GoQjQRLtsuQjcZMsA','ChIJATL2yr2rQjQRY6NG4hCfT4A',],
         '晚上' : ['ChIJm8r-jPurQjQRDP4iiEKGxVA','ChIJ2-Q7LgiqQjQRR34ZsbAsGcI','ChIJQZW6eqlTXTQRqt592n7MGdw','ChIJQZoDdT1TXTQRtjtRQi5IjSk','ChIJQcvK3JaoQjQRXfCsS_k8pgw','ChIJDznL07apQjQRfHSp2FKIklc','ChIJbQuDbJapQjQR2UzfqFzqDcA','ChIJV1KPBcWqQjQRuShpzXD669U',],
         }
    
    detail_info =  [{
        '內用座位' :  True , 
        '洗手間' :  False , 
        '無障礙' :  False , 
        '適合兒童' :  False , 
        '適合團體' :  False , 
        '現金' :  True , 
        '其他支付' :  False , 
        '收費停車' :  False , 
        '免費停車' :  False , 
        'wi-fi' :  False , 
        }]
    
    result = type_filter(condition_data, detail_info)
    print(result)
