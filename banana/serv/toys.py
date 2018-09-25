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


@toy.route("/device_toy_id", methods=["POST"])
def device_toy_id():  # 验证设备id
    RET["code"] = 0
    RET["msg"] = "开机成功"
    RET["data"] = {}

    device_id = request.form.get("device_id")  # 获取设备id

    # 判断设备id是否在设备表中
    if MONGO_DB.devices.find_one({"device_id": device_id}):
        # 查询设备id是否在玩具表中
        toy_info = MONGO_DB.toys.find_one({"device_id": device_id})
        if toy_info:
            # RET添加键值,获取玩具id
            RET["data"]["toy_id"] = str(toy_info.get("_id"))
            # 音频文件
            RET["data"]["audio"] = "success.mp3"
            return jsonify(RET)
        else:
            # 已授权的设备,但是没有绑定主人
            RET["msg"] = "找小主人"
            RET["data"]["audio"] = "Nobind.mp3"
            return jsonify(RET)
    else:
        # 不在设备表中，说明是未授权，或者是冒牌的！
        RET["msg"] = "联系玩具厂"
        RET["data"]["audio"] = "Nodevice.mp3"
        return jsonify(RET)


@toy.route("/toy_info", methods=["POST"])
def toy_info():  # 玩具管理页面
    toy_id = request.form.get("toy_id")
    print(toy_id)
    toy = MONGO_DB.toys.find_one({"_id":ObjectId(toy_id)})

    toy["_id"] = str(toy.get("_id"))

    RET["code"] = 0
    RET["msg"] = ""
    RET["data"] = toy

    return jsonify(RET)