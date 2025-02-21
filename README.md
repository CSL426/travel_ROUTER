# 🌏 Travel Router | Tibame Project

<div align="center">

![Version](https://img.shields.io/badge/version-3.2.0-blue)
![Build](https://img.shields.io/badge/build-passing-brightgreen)
![Team](https://img.shields.io/badge/team-Tibame-orange)

*AI AGENT自動化推薦助手*

</div>

## 📋 專案概述

本專案包含兩大核心系統：
- 🚗 旅遊演算法系統：智能路線規劃
- 🎯 情境搜尋系統：精準景點推薦

## 👥 團隊分工

### 旅遊演算法團隊

| 負責人 | 負責範圍 | 狀態 |
|:---|:---|:---:|
| PonPon | Line 端、LLM 端 | 🟢 |
| 石頭 | 向量搜尋端 | 🟢 |
| 瑜庭 | 關聯式搜尋端 | 🟢 |
| 啓舜 | 旅遊演算法、main_trip.py | 🟢 |

### 情境搜尋團隊

| 負責人 | 負責範圍 | 狀態 |
|:---|:---|:---:|
| PonPon | Line 端、LLM 端 | 🟢 |
| 石頭 | 向量搜尋端 | 🟢 |
| 瑜庭 | 關聯式搜尋端、情境搜尋演算法 | 🟢 |
| 家偉 | main_plan.py | 🟢 |

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
│   ├── line/      🌐 [PonPon]  - Line 端開發
│   ├── llm/       🤖 [ABBY]    - LLM 端開發
│   ├── retrieval/ 🔍 [石頭]    - 向量搜尋
│   ├── sql/       💾 [瑜庭]    - 關聯式搜尋
│   ├── plan/      📋 [瑜庭]    - 情境搜尋演算法
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

### 分支管理示意圖
![分支管理示意圖](https://github.com/user-attachments/assets/df3bc631-eb14-4bb9-bf7e-420841cc77f9)
