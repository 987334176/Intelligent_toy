from flask import Blueprint, request, jsonify
from setting import MONGO_DB
from setting import RET
from bson import ObjectId
from utils import chat_redis

cht = Blueprint("cht", __name__)


@cht.route("/chat_list", methods=["POST"])
def chat_list():  # 聊天记录列表
    user_id = request.form.get("user_id")
    friend_id = request.form.get("friend_id")
    print(friend_id)

    chat_window = MONGO_DB.chat.find_one({"user_list": {"$all": [user_id, friend_id]}})
    fri = MONGO_DB.toys.find_one({"_id": ObjectId(friend_id)})
    baby_name = fri.get("baby_name")
    cl = chat_window.get("chat_list")

    RET["code"] = 0
    RET["msg"] = baby_name
    RET["data"] = cl

    # 获取用户单个好友记录,修改redis的值
    chat_redis.get_user_msg_one(friend_id,user_id)

    return jsonify(RET)


@cht.route("/get_msg", methods=["POST"])
def get_msg():  # 获取聊天语言文件
    user_id = request.form.get("user_id")
    sender = request.form.get("sender")
    count = 1  # 初始值
    if not sender:
        msg_dict = chat_redis.get_msg_list(user_id)
        # print(msg_dict,"msg_dict")
        # 未读数量
        sender = [i for i in msg_dict.keys() if msg_dict[i] != 0 and i != "count"]
        if sender:
            sender = sender[0]
            count = msg_dict[sender]
        else:
            pass  # 没有任何消息了，可以调用合成语言，提示一下
            # filename= baidu_ai.text2audio("")
            # new_msg = [{sender:"",msg:filename}]
    else:
        # 获取用户某个好友的值
        count = chat_redis.get_user_msg_one(sender,user_id)

    # $all 表示多个条件都成立时。这里表示user_list字段中user_id和sender必须都存在才行！
    chat_window = MONGO_DB.chat.find_one({"user_list": {"$all": [user_id, sender]}})
    # [-count:] 表示获取最后的几条消息。比如： -1: 表示最后一条
    new_msg = chat_window.get("chat_list")[-count:]
    # 这里可以提示,您收到来自xx的几条消息
    # filename= baidu_ai.text2audio("")
    # new_msg.insert(0,{
    #     "sender":sender,
    #     "msg":filename
    # })

    RET["code"] = 0
    RET["msg"] = ""
    RET["data"] = new_msg

    chat_redis.get_user_msg_one(sender,user_id)

    return jsonify(RET)

@cht.route("/get_msg_list", methods=["POST"])
def get_msg_list():
    user_id = request.form.get("user_id")
    user_msg_dict = chat_redis.get_msg_list(user_id)

    RET["code"] = 0
    RET["msg"] = ""
    RET["data"] = user_msg_dict

    return jsonify(RET)
