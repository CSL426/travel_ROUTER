# Main Trip Module Documentation

## Overview
這是一個行程規劃系統，可以根據使用者的文字描述，自動規劃包含景點、餐廳的行程建議。

## Basic Usage

```python
from main.main_trip.controllers.controller import TripController
from dotenv import load_dotenv
import os

# 初始化設定
load_dotenv()
config = {
    'jina_url': os.getenv('jina_url'),
    'jina_headers_Authorization': os.getenv('jina_headers_Authorization'),
    'qdrant_url': os.getenv('qdrant_url'),
    'qdrant_api_key': os.getenv('qdrant_api_key'),
    'ChatGPT_api_key': os.getenv('ChatGPT_api_key')
}

# 建立控制器實例
controller = TripController(config)

# 處理使用者輸入
user_input = "想去台北文青的地方，吃午餐要便宜又好吃，下午想去逛有特色的景點，晚餐要可以跟朋友聚餐"
result = controller.process_message(user_input)

# 印出行程
controller.trip_planner.print_itinerary(result)
```

## 使用包裝好的函式
如果想要更簡單的使用方式，可以直接使用 `run_trip_planner` 函式：

```python
from main import run_trip_planner

user_input = "想去台北文青的地方，吃午餐要便宜又好吃，下午想去逛有特色的景點，晚餐要可以跟朋友聚餐"
result = run_trip_planner(user_input)
```

## Setup

### 環境變數設定
在 `.env` 檔案中設置以下變數：
```env
jina_url=your_jina_url
jina_headers_Authorization=your_authorization
qdrant_url=your_qdrant_url
qdrant_api_key=your_api_key
ChatGPT_api_key=your_chatgpt_api_key
```

## 系統流程
1. 使用 LLM 分析使用者意圖
2. 使用向量搜尋找出符合描述的地點
3. 根據特殊需求篩選地點
4. 規劃完整行程

## Notes
- 確保所有環境變數都已正確設置
- 需要網路連接以使用相關 API 服務
- 建議使用詳細的描述來獲得更好的規劃結果

## Error Handling
系統會回傳錯誤訊息如果：
- 環境變數未正確設置
- API 服務連接失敗
- 無法找到符合條件的地點