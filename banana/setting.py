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

# 文件目录
import os

AUDIO_FILE = os.path.join(os.path.dirname(__file__), "audio")
AUDIO_IMG_FILE = os.path.join(os.path.dirname(__file__), "audio_img")