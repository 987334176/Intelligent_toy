import requests
import json
import os
import setting
from uuid import uuid4

XMLY_URL = "http://m.ximalaya.com/tracks/"

# 从专辑列表获取的a标签的herf属性
content_url = "/ertong/424529/7713760"
category = "erge"  # 分类

# rsplit从右向左寻找，以某个元素为中心将左右分割成两个元素并放入列表中
# rsplit("/",1) 这里面的1表示分割次数,只分割一次
# [-1] 取最后一个元素
pid = content_url.rsplit("/",1)[-1]  # 获取歌曲id,也就是7713678

# 拼接url，也就是http://m.ximalaya.com/tracks/7713678.json
xiaopapa_url = XMLY_URL + pid + ".json"


content = requests.get(xiaopapa_url)  # get方式访问url
# 获取返回结果，使用content.content。由于是bytes类型，需要解码
content_dict = json.loads(content.content.decode("utf8"))

play_path = content_dict.get("play_path")  # 播放地址
cover_url = content_dict.get("cover_url")  # 图片地址

intro = content_dict.get("intro")  # 简介
nickname = content_dict.get("nickname")  # 昵称
title = content_dict.get("title")  # 标题

file_name = f"{uuid4()}"  # 随机文件名
audio = f"{file_name}.mp3"  # 音频
image = f"{file_name}.jpg"  # 图片

audio_file = requests.get(play_path).content  # 访问音频链接,获取二进制数据
with open(os.path.join(setting.AUDIO_FILE, audio), "wb") as f:
    f.write(audio_file)  # 写入文件

image_file = requests.get(cover_url).content  # 访问图片链接,获取二进制数据
with open(os.path.join(setting.AUDIO_IMG_FILE, image), "wb") as f:
    f.write(image_file)  # 写入文件

content_db = {
    "title": title,
    "nickname": nickname,
    "avatar": image,
    "audio": audio,
    "intro": intro,
    "category":category,  # 分类
    "play_count": 0  # 播放次数
}

setting.MONGO_DB.sources.insert_one(content_db)  # 插入一条数据