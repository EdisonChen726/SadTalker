import sqlite3
import datetime

# 连接到SQLite数据库（如果不存在则会创建）
conn = sqlite3.connect('meta_human.db')
cursor = conn.cursor()

current_datetime = datetime.datetime.now()

# # 创建用户表
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS user (
#         id INTEGER PRIMARY KEY,
#         user_name TEXT,
#         password TEXT
#     )
# ''')
#
# # 创建模特表
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS model (
#         id INTEGER PRIMARY KEY,
#         name TEXT,
#         file_id TEXT
#     )
# ''')
#
# # 创建音色表
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS voice_option (
#         id INTEGER PRIMARY KEY,
#         name TEXT
#     )
# ''')

# # 删除音频数据表
# cursor.execute('''
#     DROP TABLE audio_data
# ''')
#
#
# # 创建音频数据表
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS audio_data (
#         id INTEGER PRIMARY KEY,
#         voice_id INTEGER,
#         user_id INTEGER,
#         audio_text TEXT,
#         file_id TEXT
#     )
# ''')

# 创建视频数据表
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS video_data_new (
#         id INTEGER PRIMARY KEY,
#         model_id INTEGER,
#         audio_id INTEGER,
#         user_id  INTEGER,
#         video_name TEXT,
#         file_id TEXT,
#         create_time INTEGER
#     )
# ''')

# cursor.execute('INSERT INTO video_data_new (id, model_id, audio_id, user_id，video_name，file_id) SELECT id, model_id, audio_id, user_id，video_name，file_id FROM video_data')

# cursor.execute('DROP TABLE video_data')
#
# cursor.execute('ALTER TABLE video_data_new RENAME TO video_data')

# # 创建视频数据表
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS video_data (
#         id INTEGER PRIMARY KEY,
#         model_id INTEGER,
#         audio_id INTEGER,
#         user_id  INTEGER,
#         video_name TEXT,
#         file_id TEXT
#     )
# ''')
#
# # 创建文件信息表
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS file_info (
#         id TEXT PRIMARY KEY,
#         file_key TEXT
#     )
# ''')
#
# # 提交更改并关闭数据库连接
# conn.commit()
# conn.close()

