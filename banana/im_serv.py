from flask import Flask, request
from geventwebsocket.websocket import WebSocket
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
import json, os
from uuid import uuid4
from setting import AUDIO_FILE
from serv import content

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

    # 循环,接收消息
    while True:
        # 接收消息
        msg = user_socket.receive()
        print(msg)  # 打印
        if type(msg) == bytearray:
            # print(11)
            with open('123.wav','wb') as f:
                f.write(msg)  # 写入文件


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
            file_path = os.path.join(AUDIO_FILE, file_name)
            print(msg)
            with open(file_path, "wb") as f:
                f.write(msg)  # 写入文件

            # 将amr转换为mp3,因为html中的audio不支持amr
            os.system(f"ffmpeg -i {file_path} {file_path}.mp3")

        else:
            msg_dict = json.loads(msg)
            # {
            #     to_user: 123456
            #     音乐的id:12345678 # 音乐名称：987654321
            # }
            to_user = msg_dict.get("to_user")

            # res = content._content_one(content_id)
        if file_name and to_user:  # 如果文件名和发送用户同上存在时
            # 获取websocket对象
            other_user_socket = user_socket_dict.get(to_user)
            # 构造数据
            send_str = {
                "code": 0,
                "from_user": uid,
                # 后缀必须是mp3的
                "data": f"{file_name}.mp3"
            }
            # 发送数据给前端页面
            other_user_socket.send(json.dumps(send_str))
            # 最后一定要清空这2个变量，否则造成混乱
            file_name = ""
            to_user = ""


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