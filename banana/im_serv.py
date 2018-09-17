from flask import Flask, request
from geventwebsocket.websocket import WebSocket
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
import json


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
            print(11)
            with open('123.wav','wb') as f:
                f.write(msg)  # 写入文件


@app.route("/app/<uid>")
def user_app(uid):  # 手机app连接
    user_socket = request.environ.get("wsgi.websocket")  # type:WebSocket
    if user_socket:
        user_socket_dict[uid] = user_socket
        # { uid : websocket}
        print(user_socket_dict)
    while True:  # 手机听歌 把歌曲发送给 玩具 1.将文件直接发送给玩具 2.将当前听的歌曲名称或ID发送到玩具
        msg = user_socket.receive()
        msg_dict = json.loads(msg)  # 接收值，由于APP发送的是json，需要反序列化
        # {"music_name": "a6d680fe-fa80-4a54-82b8-b203f5a9c7b4.mp3", "toy_id": "123456"}
        user_id = msg_dict.get("toy_id")  # 获取toy_id
        music_name = msg_dict.get("music_name")  # 获取歌曲名
        # 从user_socket_dict这个大字典中获取
        other_user_socket = user_socket_dict.get(user_id)  # 获取APP用户的websocket对象
        # 构造数据
        send_str = {
            "code": 0,
            "from_user": uid,  # APP用户id
            "data": music_name  # 歌曲名
        }

        # 发送给web玩具页面,注意:不能是jsonify,它是针对于HTTP请求,会设置响应头
        # 这里是websocket连接,只能用json.dumps
        # print(send_str)
        other_user_socket.send(json.dumps(send_str))

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