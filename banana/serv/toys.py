from flask import Blueprint, request, jsonify
from setting import MONGO_DB
from setting import RET
from bson import ObjectId

toy = Blueprint("toy", __name__)


@toy.route("/toy_list", methods=["POST"])
def toy_list():  # 玩具列表
    user_id = request.form.get("user_id")  # 用户id
    # 查看用户信息
    user_info = MONGO_DB.users.find_one({"_id": ObjectId(user_id)})
    bind_toy = user_info.get("bind_toy")  # 获取绑定的玩具
    bind_toy_id = []  # 玩具列表
    for toy_id in bind_toy:  # 获取玩具列表中的所有玩具id
        bind_toy_id.append(ObjectId(toy_id))

    # 一次性查询多个玩具
    toys_list = list(MONGO_DB.toys.find({"_id": {"$in": bind_toy_id}}))

    for index,item in enumerate(toys_list):
        # 将_id转换为字符串
        toys_list[index]["_id"] = str(item.get("_id"))

    RET["code"] = 0
    RET["msg"] = ""
    RET["data"] = toys_list

    return jsonify(RET)
