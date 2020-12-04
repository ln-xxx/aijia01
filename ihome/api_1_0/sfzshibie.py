from aip import AipOcr
import json
 # 身份证 识别
""" 你的 APPID AK SK """
APP_ID = '23053404'
API_KEY = '4fektc6XrMhx2zVBCi74yWGo'
SECRET_KEY = 'ifOvfsPDyjs2taTwb1gGrUbNmZPV2ju4'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)



# 初始化AipFace对象
aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)

# 读取图片
filePath1 = "1.png"  # 正面
filePath2 = "2.png"  # 背面


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


options = {}
options["detect_direction"] = "true"  # 检测朝向
options["detect_risk"] = "true"
# 是否开启身份证风险类型(身份证复印件、临时身份证、身份证翻拍、修改过的身份证)功能，默认不开启

result1 = aipOcr.idcard(get_file_content(filePath1), 'front', options)
result2 = aipOcr.idcard(get_file_content(filePath2), 'back', options)
print(result1)
print(result2)
for key in result1['words_result'].keys():
    print(key + ':' + result1['words_result'][key]['words'])

for key in result2['words_result'].keys():
    print(key + ':' + result2['words_result'][key]['words'])