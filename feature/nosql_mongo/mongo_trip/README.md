# app.py或其他需要用到資料庫的地方
from feature.nosql.db_helper import db

# 直接使用 db
db.record_user_input(line_id, input_text)
db.save_plan(line_id, input_text, requirement, itinerary)