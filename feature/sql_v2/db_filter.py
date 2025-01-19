import pandas as pd
import vector_search as vector_search
import spec_demand
import place_type

def place_filter(condition_data: list, detail_info: list[dict], spec: bool, type: bool) -> list:

    place_id = vector_search.merge_id(condition_data)

    if spec == True:
        place_id = spec_demand.demand_filter(place_id, detail_info)
    
    if type == True:
        place_id = place_type.type_filter(place_id, detail_info)
    
    return place_id

# for trip
if __name__ == "__main__":

    condition_data = {
         '上午' : ['ChIJqelWmSGnQjQR0oQv0a6ZJ8o','ChIJI-NIexYdaDQRfldAuHBbwmY','ChIJ28UWAQAdaDQRBDGBOwEMJIY','ChIJHRHjiIOuQjQRwvkYlwIEcTQ','ChIJbVVGbyMdaDQRA4fwQM5a8Zo','ChIJJRIAm9CrQjQRVQMRfuCQIz8','ChIJJSMu6lauQjQRBVTCVxC25nU','ChIJvw3uhB-vQjQRmoAxj_eGZ6w',],
         '中餐' : ['ChIJzZsyrjaqQjQR9FND-RCuqXk','ChIJbR_veWKrQjQRyNk7HMd4VQQ','ChIJ56tavM-rQjQRpb_MPrkhHGQ','ChIJOSS68pquQjQRkjoarVAbQy8','ChIJtyX0fOapQjQRE-YyACXj1n4','ChIJBTFKTW9VXTQRYZ16hHDThow','ChIJ96mJRw-nQjQRvuEBDkiJ9Ns','ChIJAdiX-eEdaDQR0yp_crBU3lA',],
         '下午' : ['ChIJiz146XipQjQRPVUgvrZhIzI','ChIJQV-ginuvQjQRduARdLPHkQI','ChIJd46wSeADaDQRSAxunpx2RqI','ChIJnRQY8tUcaDQRiOI4CIQq6WM','ChIJWeThTAADaDQRCOTCy0na-ko','ChIJrbj1LIGsQjQRtl609U2spdk','ChIJszfi8aVVXTQRp8CmDFdK43A','ChIJOwf8sTypQjQR4UYi7n8NoaM',],
         '晚餐' : ['ChIJg5D8feOrQjQRQ4RKqUbpdUM','ChIJdzQVQo-pQjQRD1hZB7p9tFA','ChIJzeV8oKSuQjQR8vW2lapRpio','ChIJ-VQi78KpQjQRuem8YnBUX4c','ChIJz4fiL6WuQjQR6y15lAOjeRY','ChIJkWFgHQMCaDQRNXr5N6bL7OQ','ChIJ23IFu9GoQjQRLtsuQjcZMsA','ChIJATL2yr2rQjQRY6NG4hCfT4A',],
         '晚上' : ['ChIJm8r-jPurQjQRDP4iiEKGxVA','ChIJ2-Q7LgiqQjQRR34ZsbAsGcI','ChIJQZW6eqlTXTQRqt592n7MGdw','ChIJQZoDdT1TXTQRtjtRQi5IjSk','ChIJQcvK3JaoQjQRXfCsS_k8pgw','ChIJDznL07apQjQRfHSp2FKIklc','ChIJbQuDbJapQjQR2UzfqFzqDcA','ChIJV1KPBcWqQjQRuShpzXD669U',],
         }
    
    print('🔍 原始資料:')

    for period, places in condition_data.items():
        print(f'{period}: {places}')

    detail_info = [{
        '內用座位': False, 
        '洗手間': False, 
        '無障礙': False, 
        '適合兒童': False, 
        '適合團體': False, 
        '現金': False, 
        '其他支付': False, 
        '收費停車': False, 
        '免費停車': False, 
        'wi-fi': False,
    }]

    filtered_condition_data = {}

    for period, places in condition_data.items():

        filtered_places = list(set(place_filter(
            condition_data=condition_data,
            detail_info=detail_info,
            spec=True,
            type=True
        )))

        filtered_condition_data[period] = filtered_places

    print('\n✅ 篩選後結果:')
    for period, places in filtered_condition_data.items():
        print(f'{period}: {places}')
