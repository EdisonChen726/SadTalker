import uuid

from flask import Flask, request, jsonify, render_template, url_for
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS

import audio_generate
import ai_text
from datetime import timedelta  # 导入 timedelta
from database import meta_human_mapper
from aliyun_oss_utils import AliyunOSSClient
import time
import os
import gen_video_task
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = '123456'  # 替换为您自己的密钥
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)
jwt = JWTManager(app)

ossClient = AliyunOSSClient()

app.config['UPLOAD_FOLDER_IMAGE'] = "./temp/image"
app.config['UPLOAD_FOLDER_AUDIO'] = "./temp/audio"

CORS(app,resources={r"/*": {"origins": "*"}})

# 登录接口，验证用户名和密码，并生成JWT Token
@app.route('/v1/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = meta_human_mapper.get_user_by_user_name(username)
    current_timestamp = int(time.time())

    if user[6] != "VALID":
        return jsonify({
            "data": {},
            "success": False,
            "code": "401",
            "message": "登录失败:account status not valid"
        }), 401

    if user[5] < current_timestamp:
        return jsonify({
            "data": {},
            "success": False,
            "code": "401",
            "message": "登录失败:account is expired"
        }), 401

    if user[2] == password:
        access_token = create_access_token(identity=user[0])
        return jsonify({
            "data": {
                "jwt": access_token,
                "user_id": user[0],
                "is_admin": user[3] == "ADMIN",
                "expire_time": user[5],
                "status": user[6]
            },
            "success": True,
            "code": "200",
            "message": "登录成功"
        }), 200
    else:
        return jsonify({
            "data": {},
            "success": False,
            "code": "401",
            "message": "登录失败"
        }), 401



# 示例需要鉴权的受保护接口
@app.route('/v1/api/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({'message': f'欢迎, {current_user}! 这是一个受保护的资源'}), 200

@app.route('/v1/api/models', methods=['GET'])
@jwt_required()
def get_models():
    models = meta_human_mapper.get_all_models()
    models_list = []
    for row in models:
        file_info = meta_human_mapper.get_file_info_by_id(row[2])
        image_url = ossClient.get_file_url(file_info[1])
        model ={
            "model_id": str(row[0]),
            "name": row[1],
            "image": image_url
        }
        models_list.append(model)
    response_data = {
        "data": {
            "models": models_list
        },
        "success": True,
        "code": "200",
        "message": "成功获取数字人形象图片列表"
    }
    return jsonify(response_data), 200

@app.route('/v1/api/voice-options', methods=['GET'])
@jwt_required()
def get_voice_options():
    voice_options = meta_human_mapper.get_all_voice_options()
    voice_option_list = []
    for row in voice_options:
        voice_option = {
            "voice_id": str(row[0]),
            "name": row[1]
        }
        voice_option_list.append(voice_option)

    response_data = {
        "data": {
            "models": voice_option_list
        },
        "success": True,
        "code": "200",
        "message": "成功获取数字人音色列表"
    }
    return jsonify(response_data), 200

@app.route('/health-check', methods=['GET'])
def health_check():
    return "OK"

@app.route('/v1/api/generate-audio', methods=['POST'])
@jwt_required()
def generate_audio():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    voice_id = data.get('voice_id')
    text = data.get('text')
    file_name = str(time.time_ns())
    audio_file = audio_generate.generate_audio(text,voice_id, file_name)
    final_file_name = os.path.basename(audio_file)
    oss_file_key = "audio/"+final_file_name
    ossClient.upload_file(audio_file,oss_file_key)
    file_id = str(uuid.uuid4())
    meta_human_mapper.add_file_info(file_id, oss_file_key)
    os.remove(audio_file)
    audio_url = ossClient.get_file_url(oss_file_key)
    audio_id = meta_human_mapper.add_audio_data(voice_id, current_user_id, text, file_id)

    response_data = {
        "data": {
            "audio_id": str(audio_id),
            "audio_file": audio_url
        },
        "success": True,
        "code": "200",
        "message": "成功合成音频"
    }
    return jsonify(response_data), 200


@app.route('/v1/api/ai-text', methods=['POST'])
@jwt_required()
def generate_ai_text():
    data = request.get_json()
    text = data.get('text')
    ai_gen_text = ai_text.generate_ai_text(text)

    response_data = {
        "data": {
            "ai_text": ai_gen_text
        },
        "success": True,
        "code": "200",
        "message": "成功生成ai文案"
    }
    return jsonify(response_data), 200

@app.route('/v1/api/generate-video', methods=['POST'])
@jwt_required()
def generate_video():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    audio_id = data.get('audio_id')
    model_id = data.get('model_id')

    result = gen_video_task.generate_video_inner(audio_id,model_id,current_user_id)

    response_data = {
        "data": result,
        "success": True,
        "code": "200",
        "message": "开始生成视频"
    }
    return jsonify(response_data), 200

@app.route('/v1/api/history-videos', methods=['GET'])
@jwt_required()
def get_history_videos():
    current_user_id = get_jwt_identity()
    videos = meta_human_mapper.get_video_data_by_user(current_user_id)
    video_list = []
    for row in videos:
        file_id = row[5]
        file_info = meta_human_mapper.get_file_info_by_id(file_id)
        video_url = ossClient.get_file_url(file_info[1])
        model_id = row[1]
        model_info = meta_human_mapper.get_model_by_id(model_id)
        model_file_info = meta_human_mapper.get_file_info_by_id(model_info[2])
        video_snapshot_url = ossClient.get_file_url(model_file_info[1])

        video = {
            "video_id":row[0],
            "video_url":video_url,
            "video_snapshot_url":video_snapshot_url,
            "create_time": row[6]
        }
        video_list.append(video)
    response_data = {
        "data": video_list,
        "success": True,
        "code": "200",
        "message": "查询历史视频成功"
    }
    return jsonify(response_data), 200

def allowed_file_for_model(filename):
    # 允许的文件扩展名列表
    allowed_extensions = {'png', 'jpg', 'jpeg'}

    # 检查文件扩展名是否在允许的范围内
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def allowed_file_for_audio(filename):
    # 允许的文件扩展名列表
    allowed_extensions = {'wav', 'mp3'}

    # 检查文件扩展名是否在允许的范围内
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/v1/api/upload-audio', methods=['POST'])
@jwt_required()
def upload_audio():
    try:
        # 获取当前用户的ID
        current_user_id = get_jwt_identity()

        # 检查文件是否存在于请求中
        if 'file' not in request.files:
            return jsonify({"success": False, "message": "未选择文件"}), 400

        file = request.files['file']

        # 检查文件类型是否允许
        if file and allowed_file_for_audio(file.filename):
            # 获取文件名并确保其安全
            filename = secure_filename(file.filename)
            # 生成一个唯一的文件名，以防重复
            unique_filename = f"{current_user_id}_{filename}"

            # 保存文件到服务器
            file_path = os.path.join(app.config['UPLOAD_FOLDER_AUDIO'], unique_filename)
            file.save(file_path)

            # 上传文件到OSS
            remote_object_key = f"audio/{unique_filename}"  # OSS存储路径
            ossClient.upload_file(file_path, remote_object_key)

            file_id = str(uuid.uuid4())
            meta_human_mapper.add_file_info(file_id, remote_object_key)

            # 插入到数据库
            audio_id = meta_human_mapper.add_audio_data(None,current_user_id,None,file_id)

            response_data = {
                "data": {
                    "audio_id": audio_id
                },
                "success": True,
                "code": "200",
                "message": "成功上传音频"
            }
            return jsonify(response_data), 200
        else:
            return jsonify({"success": False, "message": "文件类型不支持"}), 400

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# @app.route('/v1/api/check_task/<task_id>', methods=['GET'])
# def check_task_status(task_id):
#     result = gen_video_task.generate_video_inner.AsyncResult(task_id)
#     if result.state == 'SUCCESS':
#         return jsonify({'status': 'completed', 'video_result': result.get()})
#     elif result.state == 'PENDING':
#         return jsonify({'status': 'pending'})
#     else:
#         return jsonify({'status': 'failed'})

@app.route('/admin/all-users', methods=['GET'])
@jwt_required()
def admin_get_users():
    current_user_id = get_jwt_identity()
    user = meta_human_mapper.get_user_by_id(current_user_id)
    if user[3] != "ADMIN":
        return jsonify({
            "data": {},
            "success": False,
            "code": "401",
            "message": "No permission"
        }), 401

    users = meta_human_mapper.get_all_user()
    user_list = []
    for row in users:
        user = {
            "user_id": str(row[0]),
            "user_name": row[1],
            "create_time": row[4],
            "expire_time": row[5],
            "status": row[6]
        }
        user_list.append(user)
    response_data = {
        "data": user_list,
        "success": True,
        "code": "200",
        "message": "成功用户列表"
    }
    return jsonify(response_data), 200

@app.route('/admin/all-models', methods=['GET'])
@jwt_required()
def admin_get_models():
    current_user_id = get_jwt_identity()
    user = meta_human_mapper.get_user_by_id(current_user_id)
    if user[3] != "ADMIN":
        return jsonify({
            "data": {},
            "success": False,
            "code": "401",
            "message": "No permission"
        }), 401

    models = meta_human_mapper.get_all_models()
    models_list = []
    for row in models:
        file_info = meta_human_mapper.get_file_info_by_id(row[2])
        image_url = ossClient.get_file_url(file_info[1])
        model ={
            "model_id": str(row[0]),
            "name": row[1],
            "image": image_url
        }
        models_list.append(model)
    response_data = {
        "data":  models_list,
        "success": True,
        "code": "200",
        "message": "成功获取数字人形象图片列表"
    }
    return jsonify(response_data), 200

@app.route('/admin/upload-model', methods=['POST'])
@jwt_required()
def upload_model():
    current_user_id = get_jwt_identity()
    user = meta_human_mapper.get_user_by_id(current_user_id)
    if user[3] != "ADMIN":
        return jsonify({
            "data": {},
            "success": False,
            "code": "401",
            "message": "No permission"
        }), 401
    try:
        # 检查文件是否存在于请求中
        if 'file' not in request.files:
            return jsonify({"success": False, "message": "未选择文件"}), 400

        file = request.files['file']

        # 检查文件类型是否允许
        if file and allowed_file_for_model(file.filename):
            # 获取文件名并确保其安全
            unique_filename = secure_filename(file.filename)

            # 保存文件到服务器
            file_path = os.path.join(app.config['UPLOAD_FOLDER_IMAGE'], unique_filename)
            file.save(file_path)

            # 上传文件到OSS
            remote_object_key = f"model/{unique_filename}"  # OSS存储路径
            ossClient.upload_file(file_path, remote_object_key)

            file_id = str(uuid.uuid4())
            meta_human_mapper.add_file_info(file_id, remote_object_key)

            # 将模特信息保存到数据库模特表
            name = request.form.get('name')

            # 插入到数据库
            model_id = meta_human_mapper.add_model(name, file_id)

            response_data = {
                "data": {
                    "model_id": model_id,
                    "name": name,
                },
                "success": True,
                "code": "200",
                "message": "成功上传模特照片"
            }
            return jsonify(response_data), 200
        else:
            return jsonify({"success": False, "message": "文件类型不支持"}), 400

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/admin/all-history-videos', methods=['GET'])
@jwt_required()
def get_all_history_videos():
    current_user_id = get_jwt_identity()
    user = meta_human_mapper.get_user_by_id(current_user_id)
    if user[3] != "ADMIN":
        return jsonify({
            "data": {},
            "success": False,
            "code": "401",
            "message": "No permission"
        }), 401
    user_id = request.args.get('user_id')
    if user_id:
        videos = meta_human_mapper.get_video_data_by_user(user_id)
    else:
        videos = meta_human_mapper.get_all_video_data()
    video_list = []
    for row in videos:
        file_id = row[5]
        file_info = meta_human_mapper.get_file_info_by_id(file_id)
        video_url = ossClient.get_file_url(file_info[1])
        model_id = row[1]
        model_info = meta_human_mapper.get_model_by_id(model_id)
        model_file_info = meta_human_mapper.get_file_info_by_id(model_info[2])
        video_snapshot_url = ossClient.get_file_url(model_file_info[1])

        video = {
            "user_id": row[3],
            "video_id": row[0],
            "video_url": video_url,
            "video_snapshot_url": video_snapshot_url,
            "create_time": row[6]
        }
        video_list.append(video)
    response_data = {
        "data": video_list,
        "success": True,
        "code": "200",
        "message": "查询历史视频成功"
    }
    return jsonify(response_data), 200

@app.route('/admin/all-history-audios', methods=['GET'])
@jwt_required()
def get_all_history_audios():
    current_user_id = get_jwt_identity()
    user = meta_human_mapper.get_user_by_id(current_user_id)
    if user[3] != "ADMIN":
        return jsonify({
            "data": {},
            "success": False,
            "code": "401",
            "message": "No permission"
        }), 401
    user_id = request.args.get('user_id')
    if user_id:
        audios = meta_human_mapper.get_audio_data_by_user(user_id)
    else:
        audios = meta_human_mapper.get_all_audio_data()
    audio_list = []
    for row in audios:
        file_id = row[4]
        file_info = meta_human_mapper.get_file_info_by_id(file_id)
        audio_url = ossClient.get_file_url(file_info[1])

        audio = {
            "user_id": row[2],
            "audio_id": row[0],
            "audio_url": audio_url
        }
        audio_list.append(audio)
    response_data = {
        "data": audio_list,
        "success": True,
        "code": "200",
        "message": "查询成功"
    }
    return jsonify(response_data), 200

@app.route('/admin/update-user', methods=['POST'])
@jwt_required()
def update_user():
    current_user_id = get_jwt_identity()
    user = meta_human_mapper.get_user_by_id(current_user_id)
    if user[3] != "ADMIN":
        return jsonify({
            "data": {},
            "success": False,
            "code": "401",
            "message": "No permission"
        }), 401
    data = request.get_json()
    user_id = data.get('user_id')
    expire_time = data.get('expire_time')
    status = data.get('status')

    current_timestamp = int(time.time())

    if status:
        meta_human_mapper.update_user_status(user_id, status)

    if expire_time:
        if expire_time > current_timestamp:
            meta_human_mapper.update_user_expire_time(user_id, expire_time)

    return jsonify({
        "data": {},
        "success": True,
        "code": "200",
        "message": "更新成功"
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
