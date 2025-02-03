from datetime import datetime

def First(data):
    current_date = datetime.now().strftime("%Y/%m/%d")
    
    # 定義交通方式對應的圖示
    transport_icons = {
        "大眾運輸": "🚌",
        "開車": "🚗",
        "騎車": "🛵",
        "步行": "🚶"
    }
    
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
        "text": "00:00",  # 改為單一時間點格式
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
        
        # 根據位置決定顯示的時間格式
        if i == 0:  # 起點
            temp_H["text"] = data[i]['start_time']
        elif i == len(data) - 1:  # 終點
            temp_H["text"] = data[i]['end_time']
        else:  # 中間點
            temp_H["text"] = '-'.join([data[i]['start_time'], data[i]['end_time']])
        
        # 取得交通資訊（只為中間點準備）
        is_middle_point = (i > 0 and i < len(data) - 1)
        if is_middle_point:
            transport_icon = transport_icons.get(data[i]['transport']['mode'], "🚗")
            transport_time = data[i]['transport'].get('time', '15')
            transport_info = {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": f"{transport_icon}{transport_time}分鐘",
                        "size": "xs",
                        "color": "#888888",
                        "flex": 5
                    }
                ],
                "margin": "sm"
            }
        else:
            transport_info = {
                "type": "box",
                "layout": "horizontal",
                "contents": [],
                "height": "0px"
            }

        # 建立地點容器
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
                # 只為中間點添加交通資訊
                transport_info if is_middle_point else {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [],
                    "height": "0px"
                }
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