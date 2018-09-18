import pymongo

client = pymongo.MongoClient(host="127.0.0.1", port=27017)
MONGO_DB = client["bananabase"]

RET = {
    # 0: false 2: True
    "code": 0,
    "msg": "",  # 提示信息
    "data": {}
}

XMLY_URL = "http://m.ximalaya.com/tracks/"  # 喜马拉雅链接
CREATE_QR_URL = "http://qr.liantu.com/api.php?text="  # 生成二维码API

# 文件目录
import os

AUDIO_FILE = os.path.join(os.path.dirname(__file__), "audio")  # 音频
AUDIO_IMG_FILE = os.path.join(os.path.dirname(__file__), "audio_img")  # 音频图片

DEVICE_CODE_PATH = os.path.join(os.path.dirname(__file__), "device_code")  # 二维码