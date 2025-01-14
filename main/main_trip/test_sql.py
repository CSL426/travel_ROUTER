from feature.sql import csv_read

condition_dict = csv_read.load_and_sample_data('./database/info_df.csv')
detail_info = [{'適合兒童': True, '無障礙': False, '內用座位': True}]
detail_info = [{'無障礙': False}]

result = csv_read.pandas_search(condition_data=condition_dict,
                                detail_info=detail_info)
print(len(result))
# print(condition_dict)