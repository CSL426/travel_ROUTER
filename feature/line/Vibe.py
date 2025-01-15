def thinking(data):
    # 定義商店評分圖標
    icon = {
        "type": "icon",
        "size": "sm",
        "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
    }

    # 定義評分文字樣式
    rating = {
        "type": "text",
        "text": "星等",  # 評分標籤
        "size": "sm",  # 文字大小
        "color": "#999999",  # 文字顏色
        "margin": "md",  # 文字外邊距
        "flex": 0  # 自動調整大小
    }

    # 定義商店名稱顯示樣式
    location = {
        "type": "text",
        "text": "地點",  # 文字內容
        "weight": "bold",  # 粗體
        "size": "xl"  # 文字大小
    }

    # 定義商店網址按鈕樣式
    url = {
        "type": "uri",  # 連結類型
        "label": "WEBSITE",  # 按鈕顯示標籤
        "uri": "地址的地圖"  # 默認地圖鏈接，稍後會替換為實際的URL
    }

    # 定義地址顯示樣式
    address = {
        "type": "text",
        "text": "地址",  # 地址文字
        "wrap": True,  # 文字換行
        "color": "#666666",  # 文字顏色
        "size": "sm",  # 文字大小
        "flex": 5  # 自動調整大小
    }

    # 建立一個空的列表，將來用來儲存所有的Bubble資料
    contents = []

    # 迭代資料中的每個店鋪資料
    for i in range(len(data)):
        # 定義店鋪名稱顯示
        temp_loc = location.copy()
        temp_loc['text'] = data[i]["placeID"]["name"]  # 將店鋪名稱替換為當前店鋪的名稱

        # 定義地址顯示
        temp_add = address.copy()
        temp_add['text'] = data[i]["placeID"]["address"]  # 將地址替換為當前店鋪的地址

        # 定義評分顯示
        temp_rat = rating.copy()
        temp_rat["text"] = str(data[i]["placeID"]["rating"])  # 將評分數字轉換為字符串，顯示在界面上

        # 定義URL按鈕顯示
        temp_url = url.copy()
        temp_url["uri"] = data[i]["placeID"]["url"]  # 將URL替換為當前店鋪的網址

        # 拼接每個店鋪的Bubble格式資料
        bubble = {
            "type": "bubble",  # 顯示為Bubble
            "hero": {
                "type": "image",  # 圖片類型
                "url": "https://lh5.googleusercontent.com/p/AF1QipOWQPqSYjeLa6NXglvxOamX9Ywx4qmer0riVj2n=w426-h240-k-no",  # 預設的圖片URL，可以根據每個店鋪動態更換
                "size": "full",  # 圖片填滿整個區域
                "aspectRatio": "20:13",  # 圖片比例
                "aspectMode": "cover",  # 視覺效果設置
                "action": {
                    "type": "uri",  # 動作類型為URI
                    "uri": "https://line.me/"  # 默認點擊圖片後的網址，可以根據需要替換為店鋪的網址
                }
            },
            "body": {
                "type": "box",  # 使用box來排列內部元素
                "layout": "vertical",  # 內部元素縱向排列
                "contents": [
                    temp_loc,  # 插入店鋪名稱
                    {
                        "type": "box",  # 評分部分使用box來放置圖標和文字
                        "layout": "baseline",  # 垂直排列
                        "margin": "md",  # 外邊距
                        "contents": [
                            icon, temp_rat  # 顯示圖標和評分
                        ]
                    },
                    {
                        "type": "box",  # 地址和時間部分使用box來放置
                        "layout": "vertical",  # 縱向排列
                        "margin": "lg",  # 外邊距
                        "spacing": "sm",  # 內部間距
                        "contents": [
                            {
                                "type": "box",  # 地址部分為一個單獨的box
                                "layout": "baseline",  # 基線對齊
                                "spacing": "sm",  # 內部間距
                                "contents": [
                                    temp_add
                                ]
                            }
                        ]
                    }
                ]
            },
            "footer": {
                "type": "box",  # 底部按鈕部分使用box
                "layout": "vertical",  # 垂直排列
                "spacing": "sm",  # 內部間距
                "contents": [
                    {
                        "type": "button",  # 按鈕類型
                        "style": "link",  # 使用連結樣式
                        "height": "sm",  # 按鈕高度設置為小
                        "action": temp_url  # 動作為跳轉到商店網址
                    }
                ]
            }
        }

        # 將每個bubble加入到contents列表中
        contents.append(bubble)
    # 返回所有的Bubble列表
    return contents