from flask import Blueprint, jsonify
from setting import MONGO_DB
from setting import RET

cont = Blueprint("cont", __name__)


@cont.route("/content_list", methods=["POST"])
def content_list():  # 内容列表
    res_list = list(MONGO_DB.sources.find({}))  # 字典转换列表

    for index, item in enumerate(res_list):  #返回 enumerate(枚举)对象
        # 由于_id是ObjectId对象,转换为字符串
        res_list[index]["_id"] = str(item.get("_id"))

    RET["code"] = 0
    RET["msg"] = ""
    RET["data"] = res_list

    return jsonify(RET)  # 返回json数据
