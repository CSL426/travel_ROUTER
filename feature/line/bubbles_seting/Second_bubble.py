# from linebot import LineBotApi
# from linebot.models import FlexSendMessage

# # Initialize LineBotApi
# line_bot_api = LineBotApi("ycb1CzJ1bZmK31jawt/M/xTgstIupOjCU5nBbyZocVshSExRmI1y3WfjPnHdWztZikHxQ4LB+RAe0HiFSkSoFW5mAmrKlCFJU92+pnnNxTgNuobrjkWL6GAoQ+cyyvvtnSH+DcDU0dL1B6FG0rsIVgdB04t89/1O/w1cDnyilFU=")


# data = [
#             {
#                 "name": "家",
#                 "start_time": "08:00",
#                 "end_time": "08:30",
#                 "duration": 30,
#                 "hours": "08:00-08:30",
#                 "transport": {
#                     "mode": "步行",
#                     "time": 0,
#                     "period": "00:00-00:00"
#                 }
#             },
#             {
#                 "name": "台北101",
#                 "start_time": "09:00",
#                 "end_time": "11:30",
#                 "duration": 150,
#                 "hours": "09:00-11:30",
#                 "transport": {
#                     "mode": "大眾運輸",
#                     "time": 15,
#                     "period": "08:45-09:00"
#                 }
#             },
#             {
#                 "name": "鼎泰豐(信義店)",
#                 "start_time": "11:32",
#                 "end_time": "13:02",
#                 "duration": 90,
#                 "hours": "11:32-13:02",
#                 "transport": {
#                     "mode": "步行",
#                     "time": 5,
#                     "period": "11:25-11:30"
#                 }
#             },
#             {
#                 "name": "信義威秀商圈",
#                 "start_time": "13:08",
#                 "end_time": "14:08",
#                 "duration": 60,
#                 "hours": "13:08-14:08",
#                 "transport": {
#                     "mode": "開車",
#                     "time": 10,
#                     "period": "13:00-13:10"
#                 }
#             }
#         ]



# # 內容資料處理
# location = {
#     "type": "text",
#     "text": "地點",
#     "size": "sm",
#     "align": "end"
# }
# H = {
#     "type": "text",
#     "text": "00:00-00:00",
#     "size": "sm",
#     "align": "start"
# }
# traffic={
#             "type": "text",
#             "text": "開車2分鐘",
#             "size": "sm",
#             "align": "start"
# }

# contents = []
# for i in range(len(data)):
#     temp_loc = location.copy()
#     temp_loc['text'] = data[i]["name"]

#     temp_H = H.copy()
#     temp_H["text"] = data[i]["hours"]
    
# # 修改交通時間顯示方式
#     temp_traffic = traffic.copy()
#     temp_traffic["text"] = f"{data[i]['transport']['mode']} {data[i]['transport']['time']}分鐘"  # 顯示如：步行5分鐘

#     contents_minimum = {
#     "type": "box",
#     "layout": "vertical", # 改為 vertical 以便將元素垂直排列
#     "spacing": "md",
#     "contents": [
#         {
#             "type": "box",
#             "layout": "horizontal",  # 水平排列 temp_H 和 temp_loc
#             "spacing": "md",
#             "contents": [temp_H, temp_loc],
#         },
#         temp_traffic
#     ]
#     }

#     contents.append(contents_minimum)

# # First_bubble 設定
# Second_bubble = {
#     "type": "bubble",
#     "body": {
#         "type": "box",
#         "layout": "vertical",
#         "spacing": "sm",
#         "contents": [
#             {
#                 "type": "text",
#                 "text": "Travel recommendations",
#                 "weight": "bold",
#                 "color": "#1DB446",
#                 "size": "sm"
#             },
#             {
#                 "type": "text",
#                 "text": "Taipei City",
#                 "weight": "bold",
#                 "size": "xxl",
#                 "margin": "xs"
#             },
#             {
#                 "type": "text",
#                 "text": "Date 2024/12/24",
#                 "size": "sm",
#                 "color": "#aaaaaa",
#                 "wrap": True,
#                 "margin": "md"
#             }
#         ]
#     }
# }

# cot={
#     "type": "box",
#     "layout": "vertical",
#     "spacing": "md",
#     "contents": contents
# }

# # 把內容加到 Second_bubble 的 body 中
# Second_bubble['body']['contents'].append(cot)

# # print(Second_bubble['body']['contents'])

# # 包裝為 FlexSendMessage
# flex_message = FlexSendMessage(alt_text="Your message", contents=Second_bubble)
# line_bot_api.push_message('U9a677f2c4ce0f02110916708e6a43332', flex_message)

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
        temp_H["text"] = data[i]["hours"]
        
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