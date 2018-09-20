from aip import AipSpeech
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 项目根目录

import sys
sys.path.append(BASE_DIR)  # 加入到系统环境变量中

import setting  # 导入setting


client = AipSpeech(setting.APP_ID,setting.API_KEY,setting.SECRET_KEY)

res = client.synthesis("硬件设备不符,请联系玩具厂商","zh",1,setting.SPEECH)

with open(os.path.join(setting.AUDIO_FILE,"Nodevice.mp3"),"wb") as f:
    f.write(res)