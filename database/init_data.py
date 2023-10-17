import meta_human_mapper
from aliyun_oss_utils import AliyunOSSClient
import uuid

# ossClient = AliyunOSSClient()
# ossClient.upload_file("../static/image/3.jpeg","model/3.jpeg")
# file_id = str(uuid.uuid4())
# meta_human_mapper.add_file_info(file_id,"/model/3.jpeg")
# meta_human_mapper.add_model("小帅",file_id)

# model = meta_human_mapper.get_model_by_id(1)
#
# file_id = model[2]
# file_info = meta_human_mapper.get_file_info_by_id(file_id)
# url = ossClient.get_file_url(file_info[1])
# print(url)

meta_human_mapper.add_voice_option("小美")
meta_human_mapper.add_voice_option("小宇")
meta_human_mapper.add_voice_option("逍遥")
meta_human_mapper.add_voice_option("丫丫")
meta_human_mapper.add_voice_option("小娇")
