from qiniu import Auth, put_data, etag
import qiniu.config

# 需要填写自己的 Access Key 和 Secret Key
access_key = 'ZY-0kEcw-KDHwrwXTSghppzWwd13LPUqdmxCQRHy'
secret_key = 'FPduj8MY_DC-M-Ts80YUtqnOKO5blD3RavSuDLZ7'


def storage(file_data):
    """
    上传文件到七牛
    :param file_data: 要上传的文件数据
    """


# 构建鉴权对象
    q = Auth(access_key, secret_key)
# 要上传的空间
    bucket_name = 'wocaonimei'
# 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, None, 3600)
    ret, info = put_data(token, None, file_data)
# print("info=",info)
# print("ret=",ret)
    if info.status_code == 200:
# 表示上传成功，返回文件名
        return ret.get("key")
    else:
        raise Exception("上传图片到七牛失败")
