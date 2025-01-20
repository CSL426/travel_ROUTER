# utils
> `placeID_list = [placeID1, placeID2, ....]`
> placeID_list 經過篩選後 縮小程較少的 placeID_list 再繼續傳遞
* ETL_dataframe = ETL_dataframe() ; 將 placeID 設成 index 的pandas dataframe

* placeID_list = classify_restaurant_or_view(  placeID_list,
                                                classify: 'restaurant'|'view',
                                                ETL_dataframe,
                                                )   ; 餐廳景點篩選  
* placeID_list = special_request(   placeID_list, 
                                    request_list: list[dict],
                                    ETL_dataframe, 
                                    )   ; 特殊需求篩選

* point = make_point(placeID, system: "trip"|"plan")    ; 製作 <旅遊推薦|情境搜索> 端要的 point

---

# 功能主函式
1. sql_pipeline.py 用法
```
class SqlPlacePipeline:
    def __init__(self, placeID_list):
        self.placeID_list = placeID_list

    def apply_classification(self, classify: 'restaurant'|'view'):  
    # 應用分類篩選（餐廳或景點）

    def apply_special_requests(self, request_list):
    # 應用特殊需求篩選

    def get_results(self):
    # 返回結果 placeID_list
```
> 連結 篩選function 可以選擇: 要篩餐廳景點 or 要篩特殊需求


2. sql.py 用法
points = sql(   input: list|dict,
                special_request_list: list[dict],
                system: "trip"|"plan",
                special_request: bool,
            )
> 1. load 進 input
> 2. 轉成 placeID_list
> 3. 呼叫 SqlPlacePipeline
> 4. points = placeID_list 迴圈 <透過 make_point 形承單個 point 加總>
> 5. return points

