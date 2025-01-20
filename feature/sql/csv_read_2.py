# 從向量搜尋跟llm那邊獲得資訊並讀取csv調度出資料(最符合的前100)
import pandas as pd
import os
import ast

import pandas as pd
import os
import ast
from dotenv import load_dotenv

def get_project_root():
    """獲取專案根目錄的路徑"""
    # 方法1：通過環境變數
    if 'TRAVEL_ROUTER_ROOT' in os.environ:
        return os.environ['TRAVEL_ROUTER_ROOT']
    
    # 方法2：嘗試向上查找包含特定文件的目錄
    current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    marker_files = ['.env', 'pyproject.toml', 'README.md']
    
    for file in marker_files:
        if os.path.exists(os.path.join(current_dir, file)):
            return current_dir
            
    # 如果都找不到，使用當前工作目錄
    return os.getcwd()

def get_database_path():
    """獲取資料庫文件路徑"""
    # 首先檢查環境變數
    load_dotenv()
    if 'DATABASE_PATH' in os.environ:
        return os.environ['DATABASE_PATH']
    
    # 如果環境變數未設置，使用預設路徑
    project_root = get_project_root()
    return os.path.join(project_root, 'database')

def pandas_search(vector_search_result: list[dict], special_requirements: list[dict]) -> list[dict]:
    '''
    結合向量資料搜尋出來的place_id與使用者提出的特殊需求，產出符合的結構資料
    '''
    try:
        # 獲取資料庫路徑
        database_path = get_database_path()
        
        # 檢查資料庫目錄是否存在
        if not os.path.exists(database_path):
            raise FileNotFoundError(f"找不到資料庫目錄：{database_path}")
        
        # 構建檔案路徑
        info_df_path = os.path.join(database_path, 'info_df.csv')
        hours_df_path = os.path.join(database_path, 'hours_df.csv')
        
        # 檢查檔案是否存在和可讀
        for file_path in [info_df_path, hours_df_path]:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"找不到檔案：{file_path}")
            if not os.access(file_path, os.R_OK):
                raise PermissionError(f"沒有權限讀取檔案：{file_path}")

        # 讀取 CSV 檔案
        info_df = pd.read_csv(info_df_path, dtype={
            'place_id': str,
            'device_cat': str,
            'device_all': str
        })
        hours_df = pd.read_csv(hours_df_path, dtype={'place_id': str})

        # 確保place_id列是字串類型，並去除空白
        info_df['place_id'] = info_df['place_id'].astype(str).str.strip()
        hours_df['place_id'] = hours_df['place_id'].astype(str).str.strip()

        # 處理向量搜尋結果
        places_data = []
        result_dict = vector_search_result[0]

        for place_id, score_info in result_dict.items():
            if isinstance(score_info, dict) and '分數' in score_info:
                places_data.append((place_id, score_info['分數']))

        # 轉換為 DataFrame
        condition_df = pd.DataFrame(places_data, columns=['place_id', 'match_score'])
        condition_df['place_id'] = condition_df['place_id'].astype(str).str.strip()

        # 合併資料
        filtered_df = pd.merge(condition_df, info_df, on='place_id', how='inner')

        if filtered_df.empty:
            print("警告：合併後的 DataFrame 為空")
            return []

        # 處理特殊需求
        true_keys = []
        requirements_dict = special_requirements[0]

        for requirement_key, requirement_value in requirements_dict.items():
            if isinstance(requirement_value, bool) and requirement_value is True:
                true_keys.append(requirement_key)

        print("需要篩選的特殊需求:", true_keys)

        # 根據特殊需求篩選資料
        if true_keys:
            filtered_df['device_cat'] = filtered_df['device_cat'].apply(lambda x: 
                ast.literal_eval(x) if isinstance(x, str) else [])

            def check_requirements(device_list):
                return all(key in device_list for key in true_keys)

            filtered_df = filtered_df[filtered_df['device_cat'].apply(check_requirements)]

        if filtered_df.empty:
            print("警告：特殊需求篩選後的 DataFrame 為空")
            return []

        # 合併營業時間資料
        filtered_df = pd.merge(filtered_df, hours_df, on='place_id', how='left')
        filtered_df = filtered_df[filtered_df['hours'].notna()]

        if filtered_df.empty:
            print("警告：加入營業時間後的 DataFrame 為空")
            return []

        # 新增 Google Maps URL
        filtered_df['url'] = "https://www.google.com/maps/place/?q=place_id:" + filtered_df['place_id']

        # 依評分排序並格式化輸出
        result = []
        top_places = filtered_df.nlargest(len(filtered_df), 'rating')

        for _, row in top_places.iterrows():
            result.append({
                'place_id': row['place_id'],
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

        return result

    except Exception as e:
        print(f"錯誤發生在：{str(e)}")
        print(f"錯誤類型：{type(e)}")
        import traceback
        print(traceback.format_exc())
        return []

if __name__ == "__main__":
    two = [{'ChIJ_4RNViOsQjQRIMcdxY-zq7E': {'分數': 0.7550653}, 'ChIJ_3kwh8-pQjQRYYdbndxxYho': {'分數': 0.6649922}, 'ChIJ_3Drk2CpQjQRj60tccm_S-c': {'分數': 0.619067}, 'ChIJ_3e32U2rQjQRYPisZQ7gO40': {'分數': 0.6181391}, 'ChIJ_7CLBKSrQjQRB9ZZ0J7v6us': {'分數': 0.61261255}, 'ChIJ_8_J_p2nQjQRz-2UuCW7crY': {'分數': 0.60500634}, 'ChIJ_6gVaWepQjQR03lcI5eYiQ4': {'分數': 0.5908276}, 'ChIJ_8DVPVqlQjQRVh0Ya9IJutQ': {'分數': 0.5819197}, 'ChIJ_6DGwtapQjQRQoNHpIwNSHk': {'分數': 0.5790238}, 'ChIJ_0ZLDFocaDQRv2cWcxD0m3g': {'分數': 0.57724255}, 'ChIJ_____5arQjQRmrr_ju481bw': {'分數': 0.5661571}, 'ChIJ_7_Mq8erQjQRyN9UIFLa8nc': {'分數': 0.56476474}, 'ChIJ_5Pj9COoQjQRpV-tKIBLtbA': {'分數': 0.5598517}, 'ChIJ_6itUgWsQjQRriwusI9z4lo': {'分數': 0.5568617}, 'ChIJ__-vgaWrQjQR2HPcrD3KZ74': {'分數': 0.5492884}, 'ChIJ_____wKqQjQRZSxHaKkcrZs': {'分數': 0.5490753}, 'ChIJ_4NIhyirQjQR-hS3QQI9rZ8': {'分數': 0.54404145}, 'ChIJ_00eH3GrQjQR78s3A93C9SI': {'分數': 0.54019725}, 'ChIJ_-1OCBYdaDQR_RHB-NbOw24': {'分數': 0.5398606}, 'ChIJ_4FX-FOvQjQRmX3PxK1rSQA': {'分數': 0.5396289}, 'ChIJ_5boPdypQjQRPAGE671e1ys': {'分數': 0.53607726}, 'ChIJ_3LZiLyvQjQR3SvEA0zV4Hk': {'分數': 0.53327787}, 'ChIJ__nlgOarQjQREEtudHpCT7w': {'分數': 0.5325712}, 'ChIJ__8_l1CpQjQRzwQd-HlG4lo': {'分數': 0.53246164}, 'ChIJ_1MF6xCoQjQRGIhbonCvaTE': {'分數': 0.52932644}, 'ChIJ_7LKp7OrQjQRZksUCxcoeSM': {'分數': 0.52882564}, 'ChIJ_0k1Uu2rQjQRHE3673mDzZw': {'分數': 0.52761424}, 'ChIJ_____zSqQjQRMnFa-u6AZ4s': {'分數': 0.5240617}, 'ChIJ_2re1N2oQjQRSUIvOgjlJfc': {'分數': 0.52368224}, 'ChIJ_____3alQjQRWlcnOtB6UYM': {'分數': 0.5204657}, 'ChIJ_____3ipQjQRg9PEmuGiDDc': {'分數': 0.51806617}, 'ChIJ_7cWLIMCaDQR8DsWrSSQF40': {'分數': 0.51740843}, 'ChIJ_____26sQjQRtCpE58Lv5go': {'分數': 0.5100505}, 'ChIJ_4-qS0hTXTQR-oEnlnTcouU': {'分數': 0.50490946}, 'ChIJ-_1rl4WpQjQRFIxRQ1xCpw0': {'分數': 0.4989054}, 'ChIJ_3qhwzWrQjQR9qdg6STTZHI': {'分數': 0.49828416}, 'ChIJ_3XAXf2oQjQR9lBSYrPavFE': {'分數': 0.4947319}, 'ChIJ______avQjQR2yhJGLY1Gto': {'分數': 0.49395204}, 'ChIJ_2igC-sDaDQRmD4bdnhX2IM': {'分數': 0.49379277}, 'ChIJ_4MUmH2uQjQRB1oN9hWrO6E': {'分數': 0.49326944}, 'ChIJ_8GXSwIDaDQRXH0qnC8FE2Q': {'分數': 0.49295995}, 'ChIJ_6cdnJ6rQjQRzdKUShSozW0': {'分數': 0.4899732}, 'ChIJ_____xQdaDQRgy0KzZieiHc': {'分數': 0.48885295}, 'ChIJ_5-34o-pQjQRvhGQPoguWUs': {'分數': 0.48775524}, 'ChIJ_4wUdisdaDQRB5T5o0zpu9M': {'分數': 0.48196587}, 'ChIJ_2DulyADaDQR03uIlrJIGbg': {'分數': 0.47897473}, 'ChIJ__1DI5MdaDQRr2xUrCx-_fY': {'分數': 0.47615904}, 'ChIJ_____7KpQjQRYZ3UQJrm0Nw': {'分數': 0.4758051}, 'ChIJ_5gjUXqqQjQRbbOW7D4WCqQ': {'分數': 0.47575706}, 'ChIJ_3vq7SCoQjQRn-RA5hKVix0': {'分數': 0.47109994},
            'ChIJ_6zEdECoQjQRE-m01EBDWn4': {'分數': 0.45590398}, 'ChIJ_4uOpL2sQjQRmWzEmSBHCYs': {'分數': 0.45511785}, 'ChIJ_7BrVgGsQjQRXXwK7w9tg9U': {'分數': 0.44934455}, 'ChIJ_3niSZuuQjQR2IAdyu_v9Lw': {'分數': 0.44773656}, 'ChIJ_4G2UGiqQjQREVZF_HKC6Bg': {'分數': 0.44074133}, 'ChIJ_8EP3U6uQjQR2GEZbf07ilw': {'分數': 0.4388756}, 'ChIJ_0vA4uWvQjQRr9ovIjcjCd8': {'分數': 0.4354281}, 'ChIJ_5VtCtioQjQRkjceKXaxmP4': {'分數': 0.43357778}, 'ChIJ_4yXuN6pQjQRAzu5k-Fg2GI': {'分數': 0.43264282}, 'ChIJ_7TmjcQDaDQR0hzmnCdj0hA': {'分數': 0.4299067}, 'ChIJ_4IXEu6nQjQRJ_HRTc1Tet4': {'分數': 0.42940608}, 'ChIJ_6iF2I6uQjQRgtTxSI4Ssyw': {'分數': 0.42595956}, 'ChIJ_3izqXqrQjQR6F1ea3qYVRI': {'分數': 0.42375317}, 'ChIJ_1RbiZCvQjQRHWDwJSOks4U': {'分數': 0.42361003}, 'ChIJ____zqesQjQRX-1jTMJMqa0': {'分數': 0.42173433}, 'ChIJ_5EDThKpQjQRf4L6uxaRpiI': {'分數': 0.42166036}, 'ChIJ_7PH1WymQjQRuHl4MlRzUQ4': {'分數': 0.42059553}, 'ChIJ_____7OpQjQRNA_qw6K6EcY': {'分數': 0.42030567}, 'ChIJ_2V75-6qQjQRCL0TYBNnC9Y': {'分數': 0.4199239}, 'ChIJ_7xNk-2vQjQRgLfQZLk-GPQ': {'分數': 0.416964}, 'ChIJ_____xuoQjQR-d8KPieSHvQ': {'分數': 0.41630045}, 'ChIJ_1wySmGpQjQRHjQAQyBy8Eo': {'分數': 0.41600662}, 'ChIJ__3noklTXTQR81XvOqEomIM': {'分數': 0.41547862}, 'ChIJ_1oQ3RgdaDQReuu9HyZ--GQ': {'分數': 0.41494054}, 'ChIJ_____3OpQjQRLKSOCZr7XmE': {'分數': 0.40811622}, 'ChIJ_03rlQeoQjQRILLyyIu3VgA': {'分數': 0.40811452}, 'ChIJ_5CXjxOpQjQRSZ1Pv6Ls_pc': {'分數': 0.4078567}, 'ChIJ_6zzCEtTXTQR5EYfZq7apU4': {'分數': 0.39986634}, 'ChIJ__seOrupQjQRJWy4mDQ93HE': {'分數': 0.3994836}, 'ChIJ_____-__ZzQRuIvU1WQmaqg': {'分數': 0.39792576}, 'ChIJ_5UUHgMCaDQRnkSPKaO1awI': {'分數': 0.39657116}, 'ChIJ_3iJrN8BaDQRceh2t6AhCag': {'分數': 0.3942505}, 'ChIJ_3YUOnOsQjQRxaKUQca9pbg': {'分數': 0.3931735}, 'ChIJ_5vT2qYdaDQRsPht9nvkmdg': {'分數': 0.38978237}, 'ChIJ_5iQH_KuQjQRPXZVxdwCYbk': {'分數': 0.38900843}, 'ChIJ_7xKPMuuQjQRzoyh0rJsnOc': {'分數': 0.38212562}, 'ChIJ_2_GKFqlQjQRGAF9qRkQYRM': {'分數': 0.38185835}, 'ChIJ__fN-IupQjQRI1iQHLUvJbI': {'分數': 0.38109392}, 'ChIJ__kRArgCaDQRxnzuqzCEKVI': {'分數': 0.3767755}, 'ChIJ_2li6YGnQjQR2HW9HwFSBgY': {'分數': 0.3645823}, 'ChIJ__kwcCqvQjQRTWOSVUTfSdk': {'分數': 0.36364573}, 'ChIJ_____0-uQjQRCtNdWBRn19k': {'分數': 0.3589446}, 'ChIJ_____2apQjQR9klrvEjIeW4': {'分數': 0.34694403}, 'ChIJ__f2mZ2rQjQRkpMMK2JyVWY': {'分數': 0.34420985}, 'ChIJ_____3aqQjQRajjMpIihQpc': {'分數': 0.34330803}, 'ChIJ_4NBrJgCaDQRMjnevq_d9Oc': {'分數': 0.33733577}, 'ChIJ_____-__ZzQR4KnO34EmpYs': {'分數': 0.31498748}, 'ChIJ_5GlALwCaDQREDte2V9B0P0': {'分數': 0.30759478}, 'ChIJ_____-__ZzQRh5ZaIvdnfGY': {'分數': 0.28798023}, 'ChIJ_6w_MLWnQjQRWXWAoBlsQE4': {'分數': 0.27316117}}]
    b = [{'內用座位': False, '洗手間': False, '適合兒童': False, '適合團體': False, '現金': False,
          '其他支付': False, '收費停車': False, '免費停車': False, 'wi-fi': False, '無障礙': False}]
    result = pandas_search(two, b)
    print(result)
