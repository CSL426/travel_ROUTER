import pandas as pd
import vector_search as vector_search

def demand_filter(condition_data: dict, detail_info: list[dict]) -> list:
    
    """
    將向量檢索的id_list，透過與ETL_df.csv合併，篩選出符合特殊需求條件的filter_list
    """
    
    id_list = vector_search.merge_id(condition_data)
    id_list = pd.DataFrame(id_list, columns=['place_id'])

    # read ETL_df.csv and merge with id_list
    ETL_df = pd.read_csv(r'data\ETL_df.csv', usecols=['place_id', 'device_cat'])
    ETL_df = pd.merge(ETL_df, id_list, on='place_id', how='inner')

    # turn detail_info into key:value
    detail_keys = ['內用座位', '洗手間', '適合兒童', '適合團體', '現金', '其他支付', '收費停車', '免費停車', 'wi-fi', '無障礙']
    detail_conditions = {key: detail_info[0].get(key, None) for key in detail_keys}

    # turn detail_conditions for True to a list
    true_keys = [key for key, value in detail_conditions.items() if value is True]

    # filter data from ETL_df
    if not true_keys:
        filtered_df = ETL_df
    else:
        filtered_df = ETL_df.copy()
        for key in true_keys:
            filtered_df = filtered_df[filtered_df['device_cat'].str.contains(key, na=False, case=False)]
    
    # place_id to list
    if 'place_id' in filtered_df.columns:
        filtered_list = filtered_df['place_id'].tolist()
    else:
        filtered_list = []

    return filtered_list

if __name__ == "__main__":
    
    # trip
    condition_data = {
         '上午' : ['ChIJqelWmSGnQjQR0oQv0a6ZJ8o','ChIJI-NIexYdaDQRfldAuHBbwmY','ChIJ28UWAQAdaDQRBDGBOwEMJIY','ChIJHRHjiIOuQjQRwvkYlwIEcTQ','ChIJbVVGbyMdaDQRA4fwQM5a8Zo','ChIJJRIAm9CrQjQRVQMRfuCQIz8','ChIJJSMu6lauQjQRBVTCVxC25nU','ChIJvw3uhB-vQjQRmoAxj_eGZ6w',],
         '中餐' : ['ChIJzZsyrjaqQjQR9FND-RCuqXk','ChIJbR_veWKrQjQRyNk7HMd4VQQ','ChIJ56tavM-rQjQRpb_MPrkhHGQ','ChIJOSS68pquQjQRkjoarVAbQy8','ChIJtyX0fOapQjQRE-YyACXj1n4','ChIJBTFKTW9VXTQRYZ16hHDThow','ChIJ96mJRw-nQjQRvuEBDkiJ9Ns','ChIJAdiX-eEdaDQR0yp_crBU3lA',],
         '下午' : ['ChIJiz146XipQjQRPVUgvrZhIzI','ChIJQV-ginuvQjQRduARdLPHkQI','ChIJd46wSeADaDQRSAxunpx2RqI','ChIJnRQY8tUcaDQRiOI4CIQq6WM','ChIJWeThTAADaDQRCOTCy0na-ko','ChIJrbj1LIGsQjQRtl609U2spdk','ChIJszfi8aVVXTQRp8CmDFdK43A','ChIJOwf8sTypQjQR4UYi7n8NoaM',],
         '晚餐' : ['ChIJg5D8feOrQjQRQ4RKqUbpdUM','ChIJdzQVQo-pQjQRD1hZB7p9tFA','ChIJzeV8oKSuQjQR8vW2lapRpio','ChIJ-VQi78KpQjQRuem8YnBUX4c','ChIJz4fiL6WuQjQR6y15lAOjeRY','ChIJkWFgHQMCaDQRNXr5N6bL7OQ','ChIJ23IFu9GoQjQRLtsuQjcZMsA','ChIJATL2yr2rQjQRY6NG4hCfT4A',],
         '晚上' : ['ChIJm8r-jPurQjQRDP4iiEKGxVA','ChIJ2-Q7LgiqQjQRR34ZsbAsGcI','ChIJQZW6eqlTXTQRqt592n7MGdw','ChIJQZoDdT1TXTQRtjtRQi5IjSk','ChIJQcvK3JaoQjQRXfCsS_k8pgw','ChIJDznL07apQjQRfHSp2FKIklc','ChIJbQuDbJapQjQR2UzfqFzqDcA','ChIJV1KPBcWqQjQRuShpzXD669U',],
         }
    
    # # plan
    # condition_data = [{
    #     "ChIJqelWmSGnQjQR0oQv0a6ZJ8o":{"分數":"1"} ,
    #     "ChIJzZsyrjaqQjQR9FND-RCuqXk":{"分數":"2"} , 
    #     "ChIJiz146XipQjQRPVUgvrZhIzI":{"分數":"3"} ,
    #     "ChIJg5D8feOrQjQRQ4RKqUbpdUM":{"分數":"4"} ,
    #     "ChIJm8r-jPurQjQRDP4iiEKGxVA":{"分數":"5"},
    #     "ChIJI-NIexYdaDQRfldAuHBbwmY":{"分數":"6"},
    #     "ChIJbR_veWKrQjQRyNk7HMd4VQQ":{"分數":"7"},
    #     "ChIJQV-ginuvQjQRduARdLPHkQI":{"分數":"8"},
    #     "ChIJdzQVQo-pQjQRD1hZB7p9tFA":{"分數":"9"},
    #     "ChIJ2-Q7LgiqQjQRR34ZsbAsGcI":{"分數":"10"},
    #     "ChIJ28UWAQAdaDQRBDGBOwEMJIY":{"分數":"11"},
    #     "ChIJ56tavM-rQjQRpb_MPrkhHGQ":{"分數":"12"},
    #     "ChIJd46wSeADaDQRSAxunpx2RqI":{"分數":"13"},
    #     "ChIJzeV8oKSuQjQR8vW2lapRpio":{"分數":"14"},
    #     "ChIJQZW6eqlTXTQRqt592n7MGdw":{"分數":"15"},
    # }]

    
    detail_info =  [{
        '內用座位' :  False , 
        '洗手間' :  False , 
        '無障礙' :  False , 
        '適合兒童' :  False , 
        '適合團體' :  False , 
        '現金' :  False , 
        '其他支付' :  False , 
        '收費停車' :  False , 
        '免費停車' :  False , 
        'wi-fi' :  False , 
        }]
    
    id_list = vector_search.merge_id(condition_data)
    result = demand_filter(condition_data, detail_info)
    print(result)
