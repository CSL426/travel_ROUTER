def merge_id (condition_data: dict):
    
    """
    合併condition_data中的id，輸出一個id_list
    """

    condition_records = []
    id_list = []

    if isinstance(condition_data, dict):
        for key, value in condition_data.items():
            for v in value:
                condition_records.append({'time': key, 'id': v})
                id_list.append(v)

    elif isinstance(condition_data, list):
        for item in condition_data:
            for key in item.keys():
                condition_records.append({'id': key, 'score': item[key]['分數']})
                id_list.append(key)

    return id_list

if __name__ == "__main__":
    
    condition_data = {
         '上午' : ['ChIJqelWmSGnQjQR0oQv0a6ZJ8o','ChIJI-NIexYdaDQRfldAuHBbwmY','ChIJ28UWAQAdaDQRBDGBOwEMJIY','ChIJHRHjiIOuQjQRwvkYlwIEcTQ','ChIJbVVGbyMdaDQRA4fwQM5a8Zo','ChIJJRIAm9CrQjQRVQMRfuCQIz8','ChIJJSMu6lauQjQRBVTCVxC25nU','ChIJvw3uhB-vQjQRmoAxj_eGZ6w',],
         '中餐' : ['ChIJzZsyrjaqQjQR9FND-RCuqXk','ChIJbR_veWKrQjQRyNk7HMd4VQQ','ChIJ56tavM-rQjQRpb_MPrkhHGQ','ChIJOSS68pquQjQRkjoarVAbQy8','ChIJtyX0fOapQjQRE-YyACXj1n4','ChIJBTFKTW9VXTQRYZ16hHDThow','ChIJ96mJRw-nQjQRvuEBDkiJ9Ns','ChIJAdiX-eEdaDQR0yp_crBU3lA',],
         '下午' : ['ChIJiz146XipQjQRPVUgvrZhIzI','ChIJQV-ginuvQjQRduARdLPHkQI','ChIJd46wSeADaDQRSAxunpx2RqI','ChIJnRQY8tUcaDQRiOI4CIQq6WM','ChIJWeThTAADaDQRCOTCy0na-ko','ChIJrbj1LIGsQjQRtl609U2spdk','ChIJszfi8aVVXTQRp8CmDFdK43A','ChIJOwf8sTypQjQR4UYi7n8NoaM',],
         '晚餐' : ['ChIJg5D8feOrQjQRQ4RKqUbpdUM','ChIJdzQVQo-pQjQRD1hZB7p9tFA','ChIJzeV8oKSuQjQR8vW2lapRpio','ChIJ-VQi78KpQjQRuem8YnBUX4c','ChIJz4fiL6WuQjQR6y15lAOjeRY','ChIJkWFgHQMCaDQRNXr5N6bL7OQ','ChIJ23IFu9GoQjQRLtsuQjcZMsA','ChIJATL2yr2rQjQRY6NG4hCfT4A',],
         '晚上' : ['ChIJm8r-jPurQjQRDP4iiEKGxVA','ChIJ2-Q7LgiqQjQRR34ZsbAsGcI','ChIJQZW6eqlTXTQRqt592n7MGdw','ChIJQZoDdT1TXTQRtjtRQi5IjSk','ChIJQcvK3JaoQjQRXfCsS_k8pgw','ChIJDznL07apQjQRfHSp2FKIklc','ChIJbQuDbJapQjQR2UzfqFzqDcA','ChIJV1KPBcWqQjQRuShpzXD669U',],
         }

    # condition_data = [{
    #     "001":{"分數":"1"} ,
    #     "002":{"分數":"2"} , 
    #     "003":{"分數":"3"} 
    #     }]
 
    result = merge_id(condition_data)
    print("result如下")
    print(result)
