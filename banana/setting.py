import pymongo
import os
import redis

# 数据库配置
client = pymongo.MongoClient(host="127.0.0.1", port=27017)
MONGO_DB = client["bananabase"]


REDIS_DB = redis.Redis(host="127.0.0.1",port=6379)

RET = {
    # 0: false 2: True
    "code": 0,
    "msg": "",  # 提示信息
    "data": {}
}

XMLY_URL = "http://m.ximalaya.com/tracks/"  # 喜马拉雅链接
CREATE_QR_URL = "http://qr.liantu.com/api.php?text="  # 生成二维码API

# 文件目录


AUDIO_FILE = os.path.join(os.path.dirname(__file__), "audio")  # 音频
AUDIO_IMG_FILE = os.path.join(os.path.dirname(__file__), "audio_img")  # 音频图片

DEVICE_CODE_PATH = os.path.join(os.path.dirname(__file__), "device_code")  # 二维码
CHAT_FILE = os.path.join(os.path.dirname(__file__), "chat")  # 聊天

# 百度AI配置
APP_ID = '11793552'
API_KEY = 'uA6sToQWcvYt2lT6qTW6WFrG'
SECRET_KEY = '5rZ1XGYMV39LQBVT4Y1yLNCsmueVe8RQ'
SPEECH = {
    "spd": 4,
    'vol': 5,
    "pit": 8,
    "per": 4
}

#图灵配置：
TL_URL = "http://openapi.tuling123.com/openapi/api/v2"
TL_DATA = {
    # 请求的类型 0 文本 1 图片 2 音频
    "reqType": 0,
    # // 输入信息(必要参数)
    "perception": {
        # 文本信息
        "inputText": {
            # 问题
            "text": "北京未来七天，天气怎么样"
        }
    },
    # 用户必要信息
    "userInfo": {
        # 图灵机器人的apikey
        "apiKey": "8fc493d348704ba4af5413e67e6fc90b",
        # 用户唯一标识
        "userId": "xiao"
    }
}