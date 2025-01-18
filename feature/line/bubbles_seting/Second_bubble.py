def Second(data):
    # 內容資料處理
    location = {
        "type": "text",
        "text": "地點",
        "size": "sm",
        "align": "end"
    }
    H = {
        "type": "text",
        "text": "00:00-00:00",
        "size": "sm",
        "align": "start"
    }
    traffic = {
        "type": "text",
        "text": "開車2分鐘",
        "size": "sm",
        "align": "start"
    }

    contents = []
    for i in range(len(data)):
        temp_loc = location.copy()
        temp_loc['text'] = data[i]["name"]

        temp_H = H.copy()
        temp_H["text"] = '-'.join([data[i]['start_time'], data[i]['end_time']])   # 停留時刻
        
        # 修改交通時間顯示方式
        temp_traffic = traffic.copy()
        temp_traffic["text"] = f"{data[i]['transport']['mode']} {data[i]['transport']['time']}分鐘"  # 顯示如：步行5分鐘

        contents_minimum = {
            "type": "box",
            "layout": "vertical",  # 改為 vertical 以便將元素垂直排列
            "spacing": "md",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",  # 水平排列 temp_H 和 temp_loc
                    "spacing": "md",
                    "contents": [temp_H, temp_loc]
                },
                temp_traffic
            ]
        }

        contents.append(contents_minimum)

    # Second_bubble 設定
    Second_bubble = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "text",
                    "text": "Travel recommendations",
                    "weight": "bold",
                    "color": "#1DB446",
                    "size": "sm"
                },
                {
                    "type": "text",
                    "text": "Taipei City",
                    "weight": "bold",
                    "size": "xxl",
                    "margin": "xs"
                },
                {
                    "type": "text",
                    "text": "Date 2024/12/24",
                    "size": "sm",
                    "color": "#aaaaaa",
                    "wrap": True,
                    "margin": "md"
                }
            ]
        }
    }

    # 行程內容
    cot = {
        "type": "box",
        "layout": "vertical",
        "spacing": "md",
        "contents": contents
    }

    # 把內容加到 Second_bubble 的 body 中
    Second_bubble['body']['contents'].append(cot)

    return Second_bubble