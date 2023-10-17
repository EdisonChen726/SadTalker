# celery.py - 定义 Celery 应用程序
import uuid
import inference
from database import meta_human_mapper
from aliyun_oss_utils import AliyunOSSClient
import os
import cv2
import numpy as np
from PIL import Image
import Wav2Lip_GFPGAN_.my_inference

ossClient = AliyunOSSClient()

def add_green_screen_background(image_path, background_color=(0, 255, 0)):
    # 打开图像文件
    image = Image.open(image_path)

    # 检查图像是否具有透明通道（Alpha通道）
    if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):

        # 创建一个新的背景图像
        width, height = image.size
        background = Image.new('RGBA', (width, height), (0, 255, 0, 255))  # 使用绿色背景

        # 将图像粘贴到新背景上
        background.paste(image, (0, 0), image)

        # 获取文件名（去除后缀）
        file_name, file_extension = os.path.splitext(image_path)
        # 生成新的后缀名
        new_extension = ".png"  # 新的后缀名，例如：.png

        # 创建新的文件名
        image_path = file_name + new_extension

        # 保存处理后的图像
        background.save(image_path)

    return image_path

def generate_video_inner(audio_id, model_id, user_id):
    # 下载音频文件到本地
    audio = meta_human_mapper.get_audio_data_by_id(audio_id)
    file_info = meta_human_mapper.get_file_info_by_id(audio[4])
    file_name = os.path.basename(file_info[1])
    local_audio_final_name = "./temp/audio/" + file_name
    ossClient.download_file(file_info[1], local_audio_final_name)

    # 下载模特图片到本地
    model = meta_human_mapper.get_model_by_id(model_id)
    file_info = meta_human_mapper.get_file_info_by_id(model[2])
    file_name = os.path.basename(file_info[1])
    local_model_final_name = "./temp/image/" + file_name
    ossClient.download_file(file_info[1], local_model_final_name)

    model_image_path = add_green_screen_background(local_model_final_name)

    video_file_name = inference.gen_video(local_audio_final_name, model_image_path, './temp/video')
    file_name = os.path.basename(video_file_name)
    oss_file_key = "video/" + file_name
    ossClient.upload_file(video_file_name, oss_file_key)
    file_id = str(uuid.uuid4())
    meta_human_mapper.add_file_info(file_id, oss_file_key)
    video_id = meta_human_mapper.add_video_data(model_id, audio_id, user_id, file_name, file_id)
    video_url = ossClient.get_file_url(oss_file_key)

    video_info = {
        "video_id":video_id,
        "video_url":video_url
    }

    return video_info