import os
from dotenv import load_dotenv
from linebot import LineBotApi
from linebot.models import FlexSendMessage, CarouselContainer, BubbleContainer
from First_bubble import First
from Second_bubble import Second
from Third_bubble import Third
from Fourth_bubble import Fourth

load_dotenv()

# 從.env檔案讀取環境變數
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_USER_ID = os.getenv("LINE_USER_ID")

# 初始化 LineBotApi 物件
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

data = [
            {
                "name": "家",
                "start_time": "08:00",
                "end_time": "08:30",
                "duration": 30,
                "hours": "08:00-08:30",
                "transport": {
                    "mode": "步行",
                    "time": 0,
                    "period": "00:00-00:00"
                }
            },
            {
                "name": "台北101",
                "start_time": "09:00",
                "end_time": "11:30",
                "duration": 150,
                "hours": "09:00-11:30",
                "transport": {
                    "mode": "大眾運輸",
                    "time": 15,
                    "period": "08:45-09:00"
                }
            },
            {
                "name": "鼎泰豐(信義店)",
                "start_time": "11:32",
                "end_time": "13:02",
                "duration": 90,
                "hours": "11:32-13:02",
                "transport": {
                    "mode": "步行",
                    "time": 5,
                    "period": "11:25-11:30"
                }
            },
            {
                "name": "信義威秀商圈",
                "start_time": "13:08",
                "end_time": "14:08",
                "duration": 60,
                "hours": "13:08-14:08",
                "transport": {
                    "mode": "開車",
                    "time": 10,
                    "period": "13:00-13:10"
                }
            }
        ]

# 創建 carousel
carousel = {
    "type": "carousel",
    "contents": [
        First(data),  # 呼叫 First_bubble 函數來獲取 bubble
        Second(data),  # 呼叫 Second_bubble 函數來獲取 bubble
        Third(data),  # 呼叫 Third_bubble 函數來獲取 bubble
        Fourth()  # 呼叫 Fourth_bubble 函數來獲取 bubble
    ]
}


# 建立 Flex 訊息
flex_message = FlexSendMessage(alt_text="Travel recommendations", contents=carousel)

# 發送訊息給 LINE 使用者
line_bot_api.push_message(LINE_USER_ID, flex_message)