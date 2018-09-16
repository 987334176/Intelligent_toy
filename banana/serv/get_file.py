from flask import Blueprint, send_file
from setting import AUDIO_FILE
from setting import AUDIO_IMG_FILE
import os

getfile = Blueprint("getfile", __name__)

@getfile.route("/get_audio/<filename>")
def get_audio(filename):  # 获取音频
    sendfile = os.path.join(AUDIO_FILE, filename)
    return send_file(sendfile)

@getfile.route("/get_image/<filename>")
def get_image(filename):  # 获取图片
    sendfile = os.path.join(AUDIO_IMG_FILE, filename)
    return send_file(sendfile)

