# CSV 資料搜尋工具

## 簡介
此專案提供 Python 腳本，能根據向量搜尋結果與使用者指定的偏好條件來搜尋與篩選地點資料。
程式會讀取包含地點資訊的 CSV 檔案，並輸出最符合需求的地點。

## 檔案說明
- **csv_read.py**：旅遊演算法使用，根據使用者偏好篩選與排序資料。
- **csv_read_2.py**：情境搜尋使用，提供更細緻的篩選與評分功能。

## 功能特色
- 將搜尋結果與詳細地點資訊合併。
- 根據使用者指定條件（如：適合兒童、有室內座位）篩選地點。
- 根據評分與符合度進行排序。
- 結果附上 Google Maps 位置連結。

## 環境需求
- Python 3.x
- pandas

## 安裝步驟
1. 複製此專案：
   ```bash
   git clone <repository-url>
   ```
2. 安裝所需套件：
   ```bash
   pip install pandas
   ```

## 使用方式
### 執行 csv_read.py
```bash
python csv_read.py
```
### 執行 csv_read_2.py
```bash
python csv_read_2.py
```

## 輸入資料
- `info_df.csv`：包含地點基本資訊。
- `hours_df.csv`：包含每個地點的營業時間資訊。

## 自訂條件
可修改腳本中的 `detail_info` 來調整篩選條件：
```python
detail_info = [{'適合兒童': True, '無障礙': False, '內用座位': True}]
```
