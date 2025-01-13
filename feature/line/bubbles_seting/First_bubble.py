
# def First(data):
#     location = {
#         "type": "text",
#         "text": "地點",
#         "size": "sm",
#         "spacing": "md",
#         "align": "end"
#     }
#     H = {
#         "type": "text",
#         "text": "00:00-00:00",
#         "size": "sm",
#         "spacing": "md",
#         "align": "start"
#     }

#     contents = []
#     for i in range(len(data)):
#         temp_loc = location.copy()
#         temp_loc['text'] = data[i]["name"]

#         temp_H = H.copy()
#         temp_H["text"] = data[i]["hours"]

#         contents_minimum = {
#             "type": "box",
#             "layout": "horizontal",
#             "spacing": "md",
#             "margin": "md",
#             "contents": [temp_H, temp_loc]
#         }

#         contents.append(contents_minimum)

#     # First_bubble 把整體的bubble框架先設定好,最後再把其他的部分加進去
#     First_bubble = {
#         "type": "bubble",
#         "body": {
#             "type": "box",
#             "layout": "vertical",
#             "spacing": "md",
#             "contents": [
#                 {
#                     "type": "text",
#                     "text": "Travel recommendations",
#                     "weight": "bold",
#                     "color": "#1DB446",
#                     "size": "sm"
#                 },
#                 {
#                     "type": "text",
#                     "text": "Taipei City",
#                     "weight": "bold",
#                     "size": "xxl",
#                     "margin": "xs"
#                 },
#                 {
#                     "type": "text",
#                     "text": "Date 2024/12/24",
#                     "size": "sm",
#                     "color": "#aaaaaa",
#                     "wrap": True,
#                     "margin": "md"
#                 }
#             ]
#         }
#     }

#     # 利用 cot 行程 contents 都裝進去
#     cot = {
#         "type": "box",
#         "layout": "vertical",
#         "spacing": "md",
#         "contents": contents
#     }

#     # 把內容加到 First_bubble 的 body 中
#     First_bubble['body']['contents'].append(cot)

#     # footer 用來設定按鈕區塊
#     footer = {
#         "type": "box",
#         "layout": "horizontal",
#         "contents": [
#             {
#                 "type": "button",
#                 "style": "primary",
#                 "action": {
#                     "type": "uri",
#                     "label": "View Map",
#                     "uri": "https://www.google.com/maps"
#                 }
#             }
#         ]
#     }
#     # 把 footer 加到 First_bubble 中
#     First_bubble['footer'] = footer

#     return First_bubble  # 返回 bubble 內容

def First(data):
    # 定義顯示標題和時間的區塊
    H = {
        "type": "text",
        "text": "00:00-00:00",
        "size": "sm",
        "spacing": "md",
        "align": "start"
    }

    contents = []
    for i in range(len(data)):
        # 定義每個地點的名稱顯示
        temp_H = H.copy()
        temp_H["text"] = data[i]["hours"]

        # 按鈕功能：點擊後會傳送訊息並移除該地點
        # button = {
        #     "type": "button",
        #     "style": "primary",  # 可選 'primary' 或 'secondary'
        #     "action": {
        #         "type": "message",  # 按鈕點擊時發送訊息
        #         "label": data[i]["name"],  # 顯示的名稱
        #         "text": f"不要{data[i]['name']}"  # 按鈕點擊時傳送的訊息
        #     }
        # }
        button ={"type": "button",
                "style": "primary",  # 可選 'primary' 或 'secondary'
                "action": {
                "type": "message",  # 按鈕點擊時發送訊息
                "label": data[i]["name"],  # 顯示的名稱
                "text": f"不要{data[i]['name']}"  # 按鈕點擊時傳送的訊息
                },
                "style": "secondary",
                "height": "sm",
                "color": "#FFFFFF",
                "gravity": "center"
                }

        # 將每個地點和按鈕整合
        contents_minimum = {
            "type": "box",
            "layout": "horizontal",
            "spacing": "md",
            "margin": "md",
            "contents": [button , temp_H]
        }

        contents.append(contents_minimum)

    # 定義 First_bubble，將所有的內容組合成一個框架
    First_bubble = {
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

    # 用 'cot' 包裹所有的地點內容
    cot = {
        "type": "box",
        "layout": "vertical",
        "spacing": "md",
        "contents": contents
    }

    # 把地點內容加進 First_bubble 的 body 中
    First_bubble['body']['contents'].append(cot)

    # 設定 footer 區塊，包含主按鈕
    footer = {
        "type": "box",
        "layout": "horizontal",
        "contents": [
            {
                "type": "button",
                "style": "primary",
                "action": {
                    "type": "uri",
                    "label": "View Map",
                    "uri": "https://www.google.com/maps"
                }
            }
        ]
    }
    # 把 footer 加到 First_bubble 中
    First_bubble['footer'] = footer

    return First_bubble  # 返回完整的 bubble 內容
