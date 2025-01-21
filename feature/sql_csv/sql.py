






def pandas_search(  
                    system: str,
                    system_input: list|dict, 
                    special_request_list: list[dict] = [],
                ) : 
    '''
    1. load 進 input => 含向量搜索端output 、 特殊要求 list 
    2. 轉成 placeID_list
    3. points = placeID_list 迴圈 <透過 make_point 形承單個 point 加總>
    4. return points
    ---

        ```
        Args :
            input : 情境搜索端的輸入 | 旅遊搜索端的輸入
            special_request_list : 特殊要求 list 
            system : "trip"|"plan"

            # ps : 若不進行 特殊要求 篩選則給 [] 值

        output :
            trip 端 : trip 端的 points
            plan 端 : plan 端的 points
        ```
    '''
    if system == 'trip':
        return __trip_system(system_input)
    elif system == 'plan':
        return __plan_system(system_input)



if __name__ == "__main__":
    trip_system_input = {   
                            'morning' : ["PlaceID1", "PlaceID2", "PlaceID3"],
                            'lunch' : ["PlaceID1", "PlaceID2", "PlaceID3"],
                            'afternoon' : ["PlaceID1", "PlaceID2", "PlaceID3"],
                            'dinner' : ["PlaceID1", "PlaceID2", "PlaceID3"],
                            'night' : ["PlaceID1", "PlaceID2", "PlaceID3"],
                        }
    
    plan_system_input = [{
                            "Place ID 1":{"分數":"int"} ,   #相似分數
                            "Place ID 2":{"分數":"int"} , 
                            "Place ID n":{"分數":"int"} 
                        }]
