from flask import Flask, request
from geventwebsocket.websocket import WebSocket
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
import json, os
from uuid import uuid4
from setting import AUDIO_FILE,CHAT_FILE
from serv import content
from utils import baidu_ai
import setting
from bson import ObjectId
import time

app = Flask(__name__)

user_socket_dict = {}  # 空字典,用来存放用户名和发送消息


@app.route("/toy/<tid>")
def toy(tid):  # 玩具连接
    # 获取请求的WebSocket对象
    user_socket = request.environ.get("wsgi.websocket")  # type:WebSocket
    if user_socket:
        # 设置键值对
        user_socket_dict[tid] = user_socket
        print(user_socket_dict)
        # {'123456': <geventwebsocket.websocket.WebSocket object at 0x00000176ABD92E18>}

    file_name = ""
    to_user = ""
    # 循环,接收消息
    while True:
        msg = user_socket.receive()
        if type(msg) == bytearray:
            file_name = f"{uuid4()}.wav"
            file_path = os.path.join(CHAT_FILE, file_name)
            with open(file_path, "wb") as f:
                f.write(msg)
        else:
            msg_dict = json.loads(msg)
            to_user = msg_dict.get("to_user")
            msg_type = msg_dict.get("msg_type")

        if to_user and file_name:
            other_user_socket = user_socket_dict.get(to_user)
            if msg_type == "ai":
                q = baidu_ai.audio2text(file_path)
                print(q)
                ret = baidu_ai.my_nlp(q, tid)
                other_user_socket.send(json.dumps(ret))
            else:
                send_str = {
                    "code": 0,
                    "from_user": tid,
                    "msg_type": "chat",
                    "data": file_name
                }

                other_user_socket.send(json.dumps(send_str))
                _add_chat(tid, to_user, send_str.get("data"))

            to_user = ""
            file_name = ""


@app.route("/app/<uid>")
def user_app(uid):  # 手机app连接
    user_socket = request.environ.get("wsgi.websocket")  # type:WebSocket
    if user_socket:
        user_socket_dict[uid] = user_socket
        # { uid : websocket}
        print(user_socket_dict)

    file_name = ""
    to_user = ""

    while True:  # 手机听歌 把歌曲发送给 玩具 1.将文件直接发送给玩具 2.将当前听的歌曲名称或ID发送到玩具
        msg = user_socket.receive()
        if type(msg) == bytearray:  # 判断类型为bytearray
            file_name = f"{uuid4()}.amr"  # 文件后缀为amr，安卓和ios通用
            file_path = os.path.join(CHAT_FILE, file_name)  # 存放在chat目录
            print(msg)
            with open(file_path, "wb") as f:
                f.write(msg)  # 写入文件

            # 将amr转换为mp3,因为html中的audio不支持amr
            os.system(f"ffmpeg -i {file_path} {file_path}.mp3")

        else:
            msg_dict = json.loads(msg)
            to_user = msg_dict.get("to_user")  # 获取目标用户

            if msg_dict.get("msg_type") == "music":
                other_user_socket = user_socket_dict.get(to_user)

                send_str = {
                    "code": 0,
                    "from_user": uid,
                    "msg_type": "music",
                    "data": msg_dict.get("data")
                }
                other_user_socket.send(json.dumps(send_str))

            # res = content._content_one(content_id)
        if file_name and to_user:  # 如果文件名和发送用户同上存在时
            # 查询玩具信息
            res = setting.MONGO_DB.toys.find_one({"_id": ObjectId(to_user)})
            # 获取friend_remark
            fri = [i.get("friend_remark") for i in res.get("friend_list") if i.get("friend_id") == uid][0]
            msg_file_name = baidu_ai.text2audio(f"你有来自{fri}的消息")

            # 获取websocket对象
            other_user_socket = user_socket_dict.get(to_user)
            # 构造数据
            send_str = {
                "code": 0,
                "from_user": uid,
                "msg_type": "chat", # 聊天类型
                # 后缀必须是mp3的
                "data": msg_file_name
            }
            # 发送数据给前端页面
            other_user_socket.send(json.dumps(send_str))
            # 添加聊天记录到数据库
            _add_chat(uid, to_user, f"{file_name}.mp3")
            # 最后一定要清空这2个变量，否则造成混乱
            file_name = ""
            to_user = ""

def _add_chat(sender, to_user, msg):  # 添加聊天记录到数据库
    chat_window = setting.MONGO_DB.chat.find_one({"user_list": {"$all": [sender, to_user]}})
    if not chat_window.get("chat_list"):
        chat_window["chat_list"] = [{
            "sender": sender,
            "msg": msg,
            "updated_at": time.time(),
        }]
        res = setting.MONGO_DB.chat.update_one({"_id": ObjectId(chat_window.get("_id"))}, {"$set": chat_window})
    else:
        chat = {
            "sender": sender,
            "msg": msg,
            "updated_at": time.time(),
        }
        res = setting.MONGO_DB.chat.update_one({"_id": ObjectId(chat_window.get("_id"))}, {"$push": {"chat_list": chat}})

    return res

if __name__ == '__main__':
    # 创建一个WebSocket服务器
    http_serv = WSGIServer(("0.0.0.0", 9528), app, handler_class=WebSocketHandler)
    # 开始监听HTTP请求
    http_serv.serve_forever()


'''
{
    "code": 0,
    "from_user": uid,  # APP用户id
    "data": music_name  # 歌曲名
}
'''