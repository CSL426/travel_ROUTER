FROM python:3.12-slim

WORKDIR /app

# 安裝必要的系統依賴，包括 fontconfig
RUN apt-get update && apt-get install -y fontconfig

# 安裝 poetry
RUN pip install --no-cache-dir poetry

# 複製所有檔案
COPY . .

# 拷貝字型檔案到容器中的適當目錄
COPY fonts/mingliu.ttc /app/fonts/mingliu.ttc

# 安裝 Python 依賴
RUN poetry install --no-interaction --no-ansi --no-root

# 設定環境變數
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

EXPOSE 8080

# 執行命令
CMD ["poetry", "run", "python", "app.py"]
