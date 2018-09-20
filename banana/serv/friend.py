from flask import Blueprint, request, jsonify
from setting import MONGO_DB
from setting import RET
from bson import ObjectId

fri = Blueprint("fri", __name__)


@fri.route("/friend_list", methods=["POST"])
def friend_list():  # 好友列表
    user_id = request.form.get("user_id")
    # 查询用户id信息
    res = MONGO_DB.users.find_one({"_id": ObjectId(user_id)})
    friend_list = res.get("friend_list")  # 获取好友列表

    RET["code"] = 0
    RET["msg"] = ""
    RET["data"] = friend_list

    return jsonify(RET)
