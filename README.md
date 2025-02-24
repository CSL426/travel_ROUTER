# 🌏 Travel Router - 路遊憩 | Tibame Project

<div align="center">

![Version](https://img.shields.io/badge/version-3.2.0-blue)
![Build](https://img.shields.io/badge/build-passing-brightgreen)
![Team](https://img.shields.io/badge/team-Tibame-orange)

***LINE AI AGENT** : 旅遊自動化推薦助手 - **路遊憩***
</div>

- 加入我們的 LINE BOT : https://line.me/R/ti/p/@645smycm
- 專案報告影片 : https://youtu.be/ELtkfRXBCJk
- 專案 DEMO 影片 : https://youtu.be/dYxGXck1jSs
- 專案簡報 : https://oqg-primary-prod-content.s3.us-east-1.amazonaws.com/uploads/pdf/1740128607092_67b8414f96f8d.pdf

## 📋 專案概述

本專案包含兩大核心系統：
- 🚗 旅遊演算法系統：智能路線規劃
- 🎯 情境搜尋系統：精準景點推薦

## ⚙️ 系統架構
- **上方** :

  上方是我們的知識庫建置，通過 selenium 的爬蟲取下全台北 google 點位評論，並通過 ETL 處理，存入向量資料庫 Qdrant與關聯式資料庫 Cloud SQL
- **下方** :

  下方是我們的混和推薦系統，從左邊開始由 user 的 query 傳遞至 LLM 做提問增強，再串接 jina embeddings 將文字向量化處理，並對向量資料庫內容作餘弦相似度比對，最後再與關聯式資料庫做類型匹配，輸出我們的超決推薦。在最右邊可以看到我們與 mongoDB 做溝通，整合使用者歷史聊天紀錄與回饋做推薦系統的增強。
![簡報v1_程珣](https://github.com/user-attachments/assets/0a219b4a-d833-41b3-9657-db8f276bbaa8)

## 👥 團隊分工

### 旅遊演算法團隊

| 負責人 | 負責範圍 | 狀態 |
|:---|:---|:---:|
| 胤鵬 | Line 端、LLM 端 | 🟢 |
| 石頭 | 向量搜索端 | 🟢 |
| 程珣 | 向量資料庫建置 | 🟢 |
| 瑜庭 | 關聯式搜尋端 | 🟢 |
| 啓舜 | 旅遊演算法、旅遊問答系統 | 🟢 |

### 情境搜尋團隊

| 負責人 | 負責範圍 | 狀態 |
|:---|:---|:---:|
| 胤鵬 | Line 端、LLM 端 | 🟢 |
| 石頭 | 向量搜尋端、情境搜索演算法 | 🟢 |
| 程珣 | 向量資料庫建置 | 🟢 |
| 瑜庭 | 關聯式搜尋端 | 🟢 |
| 家偉 | 情境搜索問答系統 | 🟢 |

## 🌳 分支管理

### 常駐分支
維護者：程珣

| 分支名稱 | 用途 | 狀態 |
|:---|:---|:---:|
| `master` (main) | 提供 release 合併，已上線分支 | 🟢 |
| `develop` | 提供穩定版本 integration 合併 | 🟡 |
| `integration` | 所有 feature 基於此分支開發 | 🔵 |

### 開發分支

#### 測試與修復分支
維護者：程珣

| 分支類型 | 用途 |
|:---|:---|
| `release/*` | 提供 develop 合併，上線前測試 |
| `hotfix/*` | release、master 分支 bug 修復 |

#### 功能開發分支
基於 `integration` 分支

```
integration/
├── feature/
│   ├── line/      🌐 [胤鵬]    - Line 端開發
│   ├── llm/       🤖 [胤鵬]    - LLM 端開發
│   ├── retrieval/ 🔍 [石頭]    - 向量搜尋
│   ├── sql/       💾 [瑜庭]    - 關聯式搜尋
│   ├── plan/      📋 [石頭]    - 情境搜尋演算法
│   └── trip/      🚗 [啓舜]    - 旅遊演算法
└── main/
    ├── main_plan/ 📊 [家偉]    - 情境搜尋主程式
    └── main_trip/ 🎯 [啓舜]    - 旅遊演算法主程式
```

## 📁 專案結構

```
project-root/
├── feature/
│   ├── line/               # Line 端各功能開發
│   ├── llm/                # LLM 端各功能開發
│   ├── retrieval/          # 向量搜尋功能開發
│   ├── sql/                # 關聯式搜尋功能開發
│   ├── plan/               # 情境搜尋演算法開發
│   └── trip/               # 旅遊演算法功能開發
├── main/
│   ├── main_plan/          # 情境搜尋演算法 main
│   └── main_trip/          # 旅遊演算法 main
└── README.md
```

## ⚠️ 開發注意事項

### 1. 模組化開發規範
- 每個功能都必須寫成獨立的 function
- 採用模組化方式建置程式碼
- 確保程式碼的可重用性和可維護性

### 2. 規範遵守要求
- 內部內容、順序、type 必須嚴格符合規範
- 不可更動既定的規範內容
- 確保介面的一致性

### 3. 參數驗證準則
- 各部位必須確認接收參數是否符合要求
- 確保介面之間的參數傳遞正確性
- 做好錯誤處理和異常管理

## 📚 文件與資源

### 接口文件
詳細的接口文件與負責人資訊請參考：
[![文件連結](https://img.shields.io/badge/📄_接口文件-點擊查看-blue)](https://docs.google.com/presentation/d/18xqwSCuFtxsEjBkQ4jkxNkvXWN2dcOt_0aOsSer9k_g/edit#slide=id.g32640ae6244_1_32)

### 分工表
![image](https://github.com/user-attachments/assets/5433077c-659a-463d-b9f5-8a80c6d8aa41)

