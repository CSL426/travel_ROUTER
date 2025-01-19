# 使用 Python 3.12 作為基礎鏡像
FROM python:3.12-slim

# 設置工作目錄
WORKDIR /app

# 安裝 Poetry
RUN pip install --no-cache-dir poetry

# 複製 Poetry 的設定檔和 pyproject.toml 檔案
COPY pyproject.toml poetry.lock /app/

# 安裝專案依賴，使用 Poetry
RUN poetry install --no-interaction --no-ansi --no-root

# 複製應用程式檔案
COPY . /app/

# 設置環境變數 (可選)
ENV PYTHONUNBUFFERED=1

# 設置環境變數 PORT 為 5000 (本地開發端口)
ENV PORT=5000

# 暴露應用端口
EXPOSE 5000

# 設置容器啟動命令，使用 Poetry 來執行應用程式
CMD ["poetry", "run", "python", "app.py"]