from datetime import datetime

def First(data):
    current_date = datetime.now().strftime("%Y/%m/%d")
    
    transport_icons = {
        "大眾運輸": "🚄",
        "開車": "🚗",
        "騎自行車": "🚲",
        "步行": "🚶"
    }
    
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
        "text": "00:00",
        "size": "sm",
        "spacing": "md",
        "align": "center",
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
        
        if i == 0:
            temp_H["text"] = data[i]['start_time']
        elif i == len(data) - 1:
            temp_H["text"] = " "+data[i]['end_time']
        else:
            temp_H["text"] = " "+'-'.join([data[i]['start_time'], data[i]['end_time']])

        # 顯示下一個目的地的交通資訊
        transport_info = {
            "type": "box",
            "layout": "horizontal",
            "contents": [],
            "height": "0px"
        }
        
        # 如果不是最後一個地點，顯示到下一個地點的交通資訊
        if i < len(data) - 1:
            next_point = data[i + 1]
            transport_icon = transport_icons.get(next_point['transport']['mode'], "🚗")
            transport_time = next_point['transport'].get('time', '15')
            transport_info = {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": f"↓ {transport_icon} {transport_time}分鐘 ↓",
                        "size": "xs",
                        "color": "#888888",
                        "flex": 5
                    }
                ],
                "margin": "sm"
            }

        location_container = {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "lg",
                    "contents": [
                        temp_H,
                        temp_loc,
                        {
                            "type": "text",
                            "text": "×",
                            "size": "md",
                            "color": "#FF6B6B",
                            "align": "center",
                            "action": {
                                "type": "postback",
                                "label": " ",
                                "data": f"cancel_{data[i]['name']}"
                            },
                            "flex": 0,
                            "weight": "bold"
                        }
                    ]
                },
                transport_info
            ],
            "paddingAll": "sm",
            "backgroundColor": "#FFFFFF",
            "cornerRadius": "lg",
            "borderWidth": "none"
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

    cot = {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "margin": "md",
        "contents": contents
    }

    First_bubble['body']['contents'].append(cot)

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