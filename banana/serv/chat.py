from flask import Blueprint, request, jsonify
from setting import MONGO_DB
from setting import RET
from bson import ObjectId

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

    return jsonify(RET)


@cht.route("/get_msg", methods=["POST"])
def get_msg():  # 获取聊天语言文件
    user_id = request.form.get("user_id")
    sender = request.form.get("sender")
    chat_window = MONGO_DB.chat.find_one({"user_list": {"$all": [user_id, sender]}})
    new_msg = chat_window.get("chat_list")[-1]

    RET["code"] = 0
    RET["msg"] = ""
    RET["data"] = new_msg.get("msg")

    return jsonify(RET)
