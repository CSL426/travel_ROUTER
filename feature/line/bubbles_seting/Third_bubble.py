def Third(data):
    location = {
        "type": "text",
        "text": "地點",
        "size": "sm",
        "align": "start"
    }
    H = {
        "type": "text",
        "text": "00:00-00:00",
        "size": "sm",
        "align": "start"
    }

    contents = []
    for i in range(len(data)):
        temp_loc = location.copy()
        temp_loc['text'] = data[i]["name"]

        temp_H = H.copy()
        temp_H["text"] = '-'.join(data[i]["hours"].values())   # 開店時間

        contents_minimum = {
        "type": "box",
        "layout": "vertical", # 改為 vertical 以便將元素垂直排列
        "spacing": "md",
        "contents": [
            {
                "type": "box",
                "layout": "horizontal",  # 水平排列 temp_H 和 temp_loc
                "spacing": "md",
                "contents": [temp_loc],
                
            },
            {
                "type": "box",
                "layout": "horizontal",  # 水平排列 temp_H 和 temp_loc
                "spacing": "md",
                "contents": [temp_H],
            },
        ]
        }
        contents.append(contents_minimum)

    Third_bubble = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
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

    cot={
        "type": "box",
        "layout": "vertical",
        "spacing": "md",
        "contents": contents
    }

    # # 把內容加到 Second_bubble 的 body 中
    Third_bubble['body']['contents'].append(cot)

    return Third_bubble