import sqlite3
import datetime
import time


# 数据库连接
def connect_to_database():
    return sqlite3.connect('./database/meta_human.db')

# 添加用户
def add_user(user_name, password):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user (user_name, password) VALUES (?, ?)", (user_name, password))
    conn.commit()
    # 使用 lastrowid 属性获取新插入记录的ID
    inserted_id = cursor.lastrowid
    conn.close()
    return inserted_id

def get_all_user():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user ORDER BY id",)
    users = cursor.fetchall()
    conn.close()
    return users

# 查询用户
def get_user_by_id(user_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_by_user_name(user_name):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE user_name = ?", (user_name,))
    user = cursor.fetchone()
    conn.close()
    return user

# 更新用户密码
def update_user_password(user_id, new_password):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("UPDATE user SET password = ? WHERE id = ?", (new_password, user_id))
    conn.commit()
    conn.close()

def update_user_status(user_id, status):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("UPDATE user SET status = ? WHERE id = ?", (status, user_id))
    conn.commit()
    conn.close()

def update_user_expire_time(user_id, expire_time):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("UPDATE user SET expire_time = ? WHERE id = ?", (expire_time, user_id))
    conn.commit()
    conn.close()

# 删除用户
def delete_user(user_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

# 添加模特
def add_model(name, file_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO model (name, file_id) VALUES (?, ?)", (name, file_id))
    conn.commit()
    # 使用 lastrowid 属性获取新插入记录的ID
    inserted_id = cursor.lastrowid
    conn.close()
    return inserted_id

# 查询模特
def get_model_by_id(model_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM model WHERE id = ?", (model_id,))
    model = cursor.fetchone()
    conn.close()
    return model

# 查询所有模特人的列表
def get_all_models():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM model")
    models = cursor.fetchall()
    conn.close()
    return models

# 更新模特信息
def update_model_name(model_id, new_name):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("UPDATE model SET name = ? WHERE id = ?", (new_name, model_id))
    conn.commit()
    conn.close()

# 删除模特
def delete_model(model_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM model WHERE id = ?", (model_id,))
    conn.commit()
    conn.close()

# 添加音色选项
def add_voice_option(name):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO voice_option (name) VALUES (?)", (name,))
    conn.commit()
    # 使用 lastrowid 属性获取新插入记录的ID
    inserted_id = cursor.lastrowid
    conn.close()
    return inserted_id

# 查询所有音色选项
def get_all_voice_options():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM voice_option")
    options = cursor.fetchall()
    conn.close()
    return options

# 添加音频数据
def add_audio_data(voice_id, user_id, audio_text, file_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO audio_data (voice_id, user_id, audio_text, file_id) VALUES (?, ?, ?, ?)",
                   (voice_id, user_id, audio_text, file_id))
    conn.commit()
    # 使用 lastrowid 属性获取新插入记录的ID
    inserted_id = cursor.lastrowid
    conn.close()
    return inserted_id

def get_audio_data_by_id(audio_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM audio_data WHERE id = ?", (audio_id,))
    audio_data = cursor.fetchone()
    conn.close()
    return audio_data

# 查询全部音频数据
def get_all_audio_data():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM audio_data ORDER BY id DESC")
    audio_data = cursor.fetchall()
    conn.close()
    return audio_data

# 查询音频数据
def get_audio_data_by_user(user_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM audio_data WHERE user_id = ?", (user_id,))
    audio_data = cursor.fetchall()
    conn.close()
    return audio_data

# 更新音频数据
def update_audio_text(audio_id, new_text):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("UPDATE audio_data SET audio_text = ? WHERE id = ?", (new_text, audio_id))
    conn.commit()
    conn.close()

# 删除音频数据
def delete_audio_data(audio_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM audio_data WHERE id = ?", (audio_id,))
    conn.commit()
    conn.close()

# 添加视频数据
def add_video_data(model_id, audio_id, user_id, video_name, file_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    current_datetime = int(time.time())
    cursor.execute("INSERT INTO video_data (model_id, audio_id, user_id, video_name, file_id, create_time) VALUES (?, ?, ?, ?, ?, ?)",
                   (model_id, audio_id, user_id, video_name, file_id, current_datetime))
    conn.commit()
    # 使用 lastrowid 属性获取新插入记录的ID
    inserted_id = cursor.lastrowid
    conn.close()
    return inserted_id

def get_all_video_data():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM video_data ORDER BY id DESC")
    video_data = cursor.fetchall()
    conn.close()
    return video_data

# 查询视频数据
def get_video_data_by_user(user_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM video_data WHERE user_id = ? ORDER BY id DESC", (user_id,))
    video_data = cursor.fetchall()
    conn.close()
    return video_data

# 更新视频名称
def update_video_name(video_id, new_name):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("UPDATE video_data SET video_name = ? WHERE id = ?", (new_name, video_id))
    conn.commit()
    conn.close()

# 删除视频数据
def delete_video_data(video_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM video_data WHERE id = ?", (video_id,))
    conn.commit()
    conn.close()


# 添加文件信息
def add_file_info(file_id, file_key):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO file_info (id, file_key) VALUES (?, ?)", (file_id, file_key))
    conn.commit()
    conn.close()

# 查询文件信息
def get_file_info_by_id(file_info_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM file_info WHERE id = ?", (file_info_id,))
    file_info = cursor.fetchone()
    conn.close()
    return file_info

# 删除文件信息
def delete_file_info(file_info_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM file_info WHERE id = ?", (file_info_id,))
    conn.commit()
    conn.close()
