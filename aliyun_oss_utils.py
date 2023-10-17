import oss2

class AliyunOSSClient:
    def __init__(self):
        # 在类内部初始化AK和SK
        self.access_key_id = 'LTAI5tDpXtmtYtVJTywQfYHV'
        self.access_key_secret = 'RJik8pyG5fX6Pmri6DudgpjE4VosIP'
        self.endpoint = 'oss-cn-hangzhou.aliyuncs.com'
        self.bucket_name = 'baiyi-shuziren'

        # 创建OSS客户端
        self.auth = oss2.Auth(self.access_key_id, self.access_key_secret)
        self.bucket = oss2.Bucket(self.auth, self.endpoint, self.bucket_name)

    def upload_file(self, local_file_path, remote_object_key):
        try:
            # 上传本地文件到OSS
            self.bucket.put_object_from_file(remote_object_key, local_file_path)
            return True
        except oss2.exceptions.OssError as e:
            print(f"文件上传失败：{str(e)}")
            return False

    def get_file_url(self, object_key, expires=36000):
        try:
            # 获取文件URL
            url = self.bucket.sign_url('GET', object_key, expires)
            https_url = url.replace("http://", "https://")
            return https_url
        except oss2.exceptions.OssError as e:
            print(f"获取文件链接失败：{str(e)}")
            return None

    def download_file(self, object_key, local_file_path):
        try:
            # 下载文件到本地
            self.bucket.get_object_to_file(object_key, local_file_path)
            return True
        except oss2.exceptions.OssError as e:
            print(f"文件下载失败：{str(e)}")
            return False