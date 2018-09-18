from flask import Blueprint, request, jsonify
from setting import MONGO_DB
from setting import RET
from bson import ObjectId

devs = Blueprint("devs", __name__)


@devs.route("/yanzheng_qr", methods=["POST"])
def yanzheng_qr():  # 验证二维码
    device_id = request.form.get("device_id")  # 获取设备id
    if MONGO_DB.devices.find_one({"device_id": device_id}):  # 从数据库中查询设备id
        # 查询该玩具是不是已被用户绑定
        toy_info = MONGO_DB.toys.find_one({"device_id": device_id})
        # 未绑定开启绑定逻辑
        if not toy_info:
            RET["code"] = 0
            RET["msg"] = "感谢购买本公司产品"
            RET["data"] = {}

        # 如果被绑定加好友逻辑开启
        if toy_info:
            pass

    else:
        RET["code"] = 2
        RET["msg"] = "二货，这不是本公司设备，快去买正版!"
        RET["data"] = {}

    return jsonify(RET)


@devs.route("/bind_toy", methods=["POST"])
def bind_toy():  # 绑定玩具
    chat_window = MONGO_DB.chat.insert_one({})  # 插入一个空数据
    chat_id = chat_window.inserted_id  # 获取聊天id

    user_id = request.form.get("user_id")  # 用户id
    res = MONGO_DB.users.find_one({"_id": ObjectId(user_id)})  # 查询用户id是否存在

    device_id = request.form.get("device_id")  # 设备id
    toy_name = request.form.get("toy_name")  # 玩具的昵称
    baby_name = request.form.get("baby_name")  # 小主人的名字
    remark = request.form.get("remark")  # 玩具主人对您的称呼
    gender = request.form.get("gender")  # 性别

    toy_info = {
        "device_id": device_id,
        "toy_name": toy_name,
        "baby_name": baby_name,
        "gender": gender,
        "avatar": "boy.jpg" if gender == 1 else "girl.jpg",
        # 绑定用户
        "bind_user": str(res.get("_id")),
        # 第一个好友
        "friend_list": [{
            "friend_id": str(res.get("_id")),  # 好友id
            "friend_name": res.get("nickname"),  # 好友昵称
            "friend_remark": remark,  # 好友称呼
            "friend_avatar": res.get("avatar"),  # 好友头像
            "friend_chat": str(chat_id),  # 好友聊天id
        }]
    }

    toy_res = MONGO_DB.toys.insert_one(toy_info)  # 插入玩具表数据

    if res.get("friend_list"):  # 判断用户好友列表是否为空
        # 追加好友
        res["bind_toy"].append(str(toy_res.inserted_id))
        res["friend_list"].append({
            "friend_id": str(toy_res.inserted_id),
            "friend_name": toy_name,
            "friend_remark": baby_name,
            "friend_avatar": toy_info.get("avatar"),
            "friend_chat": str(chat_id),
        })
    else:
        # 更新好友
        res["bind_toy"] = [str(toy_res.inserted_id)]
        res["friend_list"] = [{
            "friend_id": str(toy_res.inserted_id),
            "friend_name": toy_name,
            "friend_remark": baby_name,
            "friend_avatar": toy_info.get("avatar"),
            "friend_chat": str(chat_id),
        }]

    MONGO_DB.users.update_one({"_id": ObjectId(user_id)}, {"$set": res})  # 更新用户记录

    # 更新聊天表
    # user_list有2个值。第一个是玩具id，第2个是用户id
    # 这样，用户和玩具就能通讯了
    MONGO_DB.chat.update_one({"_id": chat_id},
                             {"$set":
                                  {"user_list":
                                       [str(toy_res.inserted_id),
                                        str(res.get("_id"))]}})

    RET["code"] = 0
    RET["msg"] = "绑定成功"
    RET["data"] = {}

    return jsonify(RET)
