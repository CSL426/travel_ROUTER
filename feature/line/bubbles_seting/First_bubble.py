from datetime import datetime

def First(data):
    current_date = datetime.now().strftime("%Y/%m/%d")
    
    # 定義顯示標題和時間的區塊
    location = {
        "type": "text",
        "text": "地點",
        "size": "sm",
        "spacing": "md",
        "align": "start",
        "wrap": True,
        "flex": 3,
        "maxLines": 2,
        "weight": "regular",
        "color": "#555555"
    }
    H = {
        "type": "text",
        "text": "00:00-00:00",
        "size": "sm",
        "spacing": "md",
        "align": "start",
        "flex": 2,
        "adjustMode": "shrink-to-fit",
        "color": "#666666",
        "weight": "regular"
    }

    contents = []
    for i in range(len(data)):
        temp_loc = location.copy()
        temp_loc['text'] = data[i]["name"]
        temp_H = H.copy()
        temp_H["text"] = '-'.join([data[i]['start_time'], data[i]['end_time']])

        cancel_button = {
            "type": "text",
            "text": "×",
            "size": "md",
            "color": "#FF6B6B",
            "align": "center",
            "action": {
                "type": "postback",
                "label": f"不要{data[i]['name']}",
                "data": f"cancel_{data[i]['name']}"
            },
            "flex": 0,
            "weight": "bold"
        }

        # 每個地點的容器
        location_container = {
            "type": "box",
            "layout": "horizontal",
            "spacing": "lg",
            "margin": "md",
            "contents": [
                temp_H,
                temp_loc,
                cancel_button
            ],
            "paddingAll": "sm",
            "backgroundColor": "#FFFFFF",
            "cornerRadius": "lg",
            "borderWidth": "none",
            "justifyContent": "space-between"
        }

        contents.append(location_container)

    First_bubble = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "backgroundColor": "#F8F9FA",
            "paddingAll": "xl",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "Travel recommendations",
                            "weight": "bold",
                            "color": "#2ECC71",
                            "size": "md",
                            "decoration": "none",
                            "align": "center"
                        }
                    ],
                    "backgroundColor": "#E8F8F5",
                    "paddingAll": "sm",
                    "cornerRadius": "lg",
                    "margin": "none"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "📍 Taipei City",
                            "weight": "bold",
                            "size": "xxl",
                            "align": "center",
                            "color": "#2C3E50"
                        }
                    ],
                    "margin": "lg"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": "📅",
                            "size": "sm",
                            "align": "center"
                        },
                        {
                            "type": "text",
                            "text": current_date,
                            "size": "sm",
                            "color": "#95A5A6",
                            "margin": "sm"
                        }
                    ],
                    "margin": "md",
                    "justifyContent": "center"
                },
                {
                    "type": "separator",
                    "margin": "xl",
                    "color": "#E9ECEF"
                }
            ]
        },
        "styles": {
            "body": {
                "backgroundColor": "#F8F9FA"
            }
        }
    }

    # 地點列表容器
    cot = {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "margin": "md",
        "contents": contents
    }

    First_bubble['body']['contents'].append(cot)

    # Footer 設定
    footer = {
        "type": "box",
        "layout": "horizontal",
        "spacing": "md",
        "margin": "none",
        "contents": [
            {
                "type": "button",
                "style": "primary",
                "action": {
                    "type": "postback",
                    "label": "收藏行程",
                    "data": "save_schedule"
                },
                "color": "#FF8DA1",
                "flex": 1,
                "height": "sm"
            },
            {
                "type": "button",
                "style": "primary",
                "action": {
                    "type": "uri",
                    "label": "地圖網址",
                    "uri": "https://www.google.com/maps"
                },
                "color": "#5C7AEA",
                "flex": 1,
                "height": "sm"
            }
        ],
        "paddingAll": "lg",
        "backgroundColor": "#F8F9FA"
    }
    
    First_bubble['footer'] = footer

    return First_bubble