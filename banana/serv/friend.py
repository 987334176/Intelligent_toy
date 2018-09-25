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

@fri.route("/add_req", methods=["POST"])
def add_req():  # 添加好友请求
    user_id = request.form.get("user_id")  # 有可能是 toy_id or user_id
    friend_id = request.form.get("friend_id")  # 100%是toy_id
    req_type = request.form.get("req_type")
    req_msg = request.form.get("req_msg")  # 描述
    remark = request.form.get("remark")  # 备注

    if req_type == "toy":
        user_info = MONGO_DB.toys.find_one({"_id": ObjectId(user_id)})
    else:
        user_info = MONGO_DB.users.find_one({"_id": ObjectId(user_id)})

    req_str = {
        "req_user": str(user_info.get("_id")),
        "req_type": req_type,
        "req_toy": friend_id,
        "req_msg": req_msg,
        "avatar": user_info.get("avatar"),
        "user_remark": remark,
        # 昵称，玩具是没有的
        "user_nick": user_info.get("nickname") if user_info.get("nickname") else user_info.get("baby_name"),
        # 状态，1通过，2拒绝,0中间状态(可切换到1和2)。
        "status": 0
    }

    MONGO_DB.req.insert_one(req_str)

    RET["code"] = 0
    RET["msg"] = "请求发送成功"
    RET["data"] = {}

    return jsonify(RET)

@fri.route("/req_list", methods=["POST"])
def req_list():  # 添加请求列表
    user_id = request.form.get("user_id")
    user_info = MONGO_DB.users.find_one({"_id": ObjectId(user_id)})
    bind_toy = user_info.get("bind_toy")

    reqs = list(MONGO_DB.req.find({"req_toy": {"$in": bind_toy}, "status": 0}))

    for index, req in enumerate(reqs):
        reqs[index]["_id"] = str(req.get("_id"))

    RET["code"] = 0
    RET["msg"] = ""
    RET["data"] = reqs

    return jsonify(RET)


@fri.route("/get_req", methods=["POST"])
def get_req():  # 获取一个好友请求
    req_id = request.form.get("req_id")

    req_info = MONGO_DB.req.find_one({"_id": ObjectId(req_id)})

    req_info["_id"] = str(req_info.get("_id"))

    RET["code"] = 0
    RET["msg"] = ""
    RET["data"] = req_info

    return jsonify(RET)


@fri.route("/acc_req", methods=["POST"])
def acc_req():  # 允许一个好友请求
    req_id = request.form.get("req_id")
    remark = request.form.get("remark")

    req_info = MONGO_DB.req.find_one({"_id": ObjectId(req_id)})

    # 1. 为 user 或 toy 添加 toy
    if req_info.get("req_type") == "toy":
        user_info = MONGO_DB.toys.find_one({"_id": ObjectId(req_info.get("req_user"))})
    else:
        user_info = MONGO_DB.users.find_one({"_id": ObjectId(req_info.get("req_user"))})

    toy = MONGO_DB.toys.find_one({"_id": ObjectId(req_info.get("req_toy"))})

    chat_window = MONGO_DB.chat.insert_one({"user_list": [str(toy.get("_id")), str(user_info.get("_id"))]})

    friend_info = {
        "friend_id": str(toy.get("_id")),
        "friend_name": toy.get("baby_name"),
        "friend_remark": req_info.get("user_remark"),
        "friend_avatar": toy.get("avatar"),
        "friend_chat": str(chat_window.inserted_id)
    }

    if req_info.get("req_type") == "toy":
        MONGO_DB.toys.update_one({"_id": ObjectId(req_info.get("req_user"))},
                                 {"$push": {"friend_list": friend_info}})
    else:
        MONGO_DB.users.update_one({"_id": ObjectId(req_info.get("req_user"))},
                                  {"$push": {"friend_list": friend_info}})

    # 2. 为 toy 添加 user 或 toy
    user_name = user_info.get("nickname") if user_info.get("nickname") else user_info.get("baby_name")
    friend_info2 = {
        "friend_id": str(user_info.get("_id")),
        "friend_name": user_name,
        # 同意方的备注
        "friend_remark": remark if remark else user_name,
        "friend_avatar": user_info.get("avatar"),
        "friend_chat": str(chat_window.inserted_id)
    }

    MONGO_DB.toys.update_one({"_id": ObjectId(req_info.get("req_toy"))},
                             {"$push": {"friend_list": friend_info2}})


    RET["code"] = 0
    RET["msg"] = f"添加好友{remark}成功"
    RET["data"] = {}

    MONGO_DB.req.update_one({"_id": ObjectId(req_id)}, {"$set": {"status": 1}})

    return jsonify(RET)


@fri.route("/ref_req", methods=["POST"])
def ref_req():  # 拒绝一个好友请求
    req_id = request.form.get("req_id")

    MONGO_DB.req.update_one({"_id": ObjectId(req_id)}, {"$set": {"status": 2}})

    RET["code"] = 0
    RET["msg"] = "已拒绝好友请求"
    RET["data"] = {}

    return jsonify(RET)
