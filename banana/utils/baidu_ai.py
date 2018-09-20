from aip import AipSpeech
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 项目根目录

import sys
sys.path.append(BASE_DIR)  # 加入到系统环境变量中

import setting  # 导入setting
from uuid import uuid4
# from setting import MONGO_DB
# import setting
import os
from bson import ObjectId

client = AipSpeech(setting.APP_ID,setting.API_KEY,setting.SECRET_KEY)

def text2audio(text):
    res = client.synthesis(text, "zh", 1, setting.SPEECH)
    file_name = f"{uuid4()}.mp3"
    file_path = os.path.join(setting.CHAT_FILE, file_name)
    with open(file_path, "wb") as f:
        f.write(res)

    return file_name


def get_file_content(filePath):
    os.system(f"ffmpeg -y -i {filePath}  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 {filePath}.pcm")
    with open(f"{filePath}.pcm", 'rb') as fp:
        return fp.read()


def audio2text(file_name):
    # 识别本地文件
    liu = get_file_content(file_name)

    res = client.asr(liu, 'pcm', 16000, {
        'dev_pid': 1536,
    })

    if res.get("result"):
        return res.get("result")[0]
    else:
        return res

# text2audio("你好")

def my_nlp(q,toy_id):
    # 1. 假设玩具说：q = 我要给爸爸发消息
    print(q,"百度q")
    if "发消息" in q:
        toy = setting.MONGO_DB.toys.find_one({"_id":ObjectId(toy_id)})
        print(toy.get("friend_list"))
        for i in toy.get("friend_list"):
            if i.get("friend_remark") in q or i.get("friend_name") in q :
                res = text2audio(f"可以按消息键，给{i.get('friend_remark')}发消息了")
                send_str = {
                    "code": 0,
                    "from_user": i.get("friend_id"),
                    "msg_type": "chat",
                    "data": res
                }
                return send_str

    if "我要听" in q or "我想听" in q or "唱一首" in q:
        sources = setting.MONGO_DB.sources.find({})
        for i in sources:
            if i.get("title") in q:
                send_str = {
                    "code": 0,
                    "from_user": toy_id,
                    "msg_type": "music",
                    "data": i.get("audio")
                }
                return send_str



    res = text2audio("对不起，我没明白你的意思")
    send_str = {
        "code": 0,
        "from_user": toy_id,
        "msg_type": "chat",
        "data": res
    }
    return send_str