from datetime import datetime
from typing import List, Dict


def First(data: List[Dict], plan_index: int = 1):
    current_date = datetime.strptime(
        data[0]['date'], "%Y-%m-%d").strftime("%Y/%m/%d")

    transport_icons = {
        "大眾運輸": "🚄",
        "開車": "🚗",
        "騎自行車": "🚲",
        "步行": "🚶"
    }

    contents = []
    for i in range(len(data)):
        # 生成URL
        location_url = ""
        if data[i].get('place_id'):
            location_url = f"https://www.google.com/maps/search/?api=1&query=Google&query_place_id={data[i]['place_id']}"
        else:
            location_url = f"https://www.google.com/maps/search/?api=1&query={data[i]['lat']},{data[i]['lon']}"

        time_text = ""
        # 設定停留區間
        if i == 0:
            time_text = data[i]['start_time']
        elif i == len(data) - 1:
            time_text = " " + data[i]['end_time']
        else:
            time_text = " " + \
                '-'.join([data[i]['start_time'], data[i]['end_time']])

        time_contents = []
        time_contents.append(
            {
                "type": "text",
                "text": time_text,
                "size": "sm",
                "align": "center",  # 單行文字置中
                "flex": 1,
                "adjustMode": "shrink-to-fit",
                "color": "#666666",
                "weight": "regular",
            }
        )

        # 如果不是最後一個地點，顯示到下一個地點的交通資訊
        if i < len(data) - 1:
            next_point = data[i + 1]
            transport_icon = transport_icons.get(
                next_point['transport']['mode'], "🚗")
            transport_time = next_point['transport'].get('time', '15')

            # 交通時間
            time_contents.append(
                {
                    "type": "text",
                    "text": f"↓ {transport_icon} {transport_time}分鐘 ↓",
                    "size": "xs",
                    "align": "center",  # 單行文字置中
                    "color": "#888888",
                    "flex": 1,
                }
            )

            time_box = {
                "type": "box",
                "layout": "vertical",
                "contents": time_contents,
                "alignItems": "center",
                "flex": 2,
                "justifyContent": "space-between",
                # "width":"",
            }

        elif i == len(data) - 1:
            time_box = {
                "type": "box",
                "layout": "vertical",
                "contents": time_contents,
                "alignItems": "center",
                "flex": 2
            }

        # time_box = {
        #     "type": "box",
        #     "layout": "vertical",  # 垂直排列
        #     "contents": time_contents,
        #     "alignItems": "center",  # 內容水平置中
        #     "flex": 2,
        # }

        location_container = {
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": [
                time_box,
                {
                    "type": "text",
                    "text": data[i]["name"],
                    "size": "lg",
                    "spacing": "md",
                    "align": "start",
                    "gravity": "center",
                    "wrap": True,
                    "flex": 4,
                    "maxLines": 2,
                    "weight": "regular",
                    "color": "#555555",
                    "action": {
                            "type": "uri",
                            "uri": location_url
                    }
                },
                {
                    "type": "text",
                    "text": "×",
                    "size": "4xl",
                    "color": "#FF6B6B",
                    "align": "center",
                    "gravity": "center",
                    "action": {
                            "type": "postback",
                            "label": " ",
                            "data": f"cancel_{plan_index}_{data[i]['step']}_{data[i]['name']}_{data[i]['label']}"
                    },
                    "flex": 0,
                    "weight": "bold",
                    "margin": "lg",
                    # "offsetTop": "-3px",
                },
            ],
            "alignItems": "center",
            "paddingAll": "none",
            "backgroundColor": "#FFFFFF",
            "cornerRadius": "md",
            "borderWidth": "none",
            "height": "53px"
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
                            "text": "📍 一日遊行程",
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
        "size": "giga",
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
        "margin": "lg",
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
                    "type": "uri",
                    "label": "地圖網址",
                    "uri": generate_maps_url(data)
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


def generate_maps_url(data: List[Dict]) -> str:
    """產生Google Maps導航URL

    Args:
        data: List[Dict] - 地點列表

    Returns:
        str: 導航URL
    """
    import urllib.parse

    # 基本URL
    base = "https://www.google.com/maps/dir/?api=1&language=zh-TW"

    # 交通方式
    mode = data[0].get('transport', {}).get('mode_eng', 'driving')
    url = f"{base}&travelmode={mode}"

    # 起點(經緯度,不加括號)
    url += f"&origin={data[0]['lat']},{data[0]['lon']}"

    # 中途點
    if len(data) > 2:
        waypoints = []
        for place in data[1:-1]:
            waypoints.append(f"{place['lat']},{place['lon']}")

        url += f"&waypoints={urllib.parse.quote('|'.join(waypoints))}"

    # 終點(經緯度,不加括號)
    if len(data) > 1:
        url += f"&destination={data[-1]['lat']},{data[-1]['lon']}"
    print(url)
    return url
