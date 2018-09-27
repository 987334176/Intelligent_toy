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
from utils import lowB_plus
from pypinyin import lazy_pinyin, TONE2
from utils import tuling

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
    if "发消息" in q:
        q = "".join(lazy_pinyin(q, style=TONE2))
        print(q)
        toy = setting.MONGO_DB.toys.find_one({"_id": ObjectId(toy_id)})
        # print(toy.get("friend_list"))
        for i in toy.get("friend_list"):
            # 转换成拼音,即使同音字也能匹配
            remark_pinyin = "".join(lazy_pinyin(i.get("friend_remark"), style=TONE2))
            name_pinyin = "".join(lazy_pinyin(i.get("friend_name"), style=TONE2))
            print(name_pinyin)
            if remark_pinyin in q or name_pinyin in q:
                res = text2audio(f"可以按消息键，给{i.get('friend_remark')}发消息了")
                send_str = {
                    "code": 0,
                    "from_user": i.get("friend_id"),
                    "msg_type": "chat",
                    "data": res,
                    "user_type":i.get("user_type")
                }
                return send_str

    if "我要听" in q or "我想听" in q or "唱一首" in q:
        q = str(q).replace("我要听", "")
        q = str(q).replace("我想听", "")
        q = str(q).replace("唱一首", "")
        print(q)
        title = lowB_plus.my_nlp(q)
        sources = setting.MONGO_DB.sources.find_one({"title": title})
        for i in sources:
            if i.get("title") in q:
                send_str = {
                    "code": 0,
                    "from_user": toy_id,
                    "msg_type": "music",
                    "data": i.get("audio")
                }
                return send_str

    answer = tuling.to_tuling(q, toy_id)

    res = text2audio(answer)
    send_str = {
        "code": 0,
        "from_user": toy_id,
        "msg_type": "chat",
        "data": res
    }
    return send_str