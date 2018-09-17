from flask import Blueprint, jsonify,request
from setting import MONGO_DB
from setting import RET
from bson import ObjectId

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


@cont.route("/content_one", methods=["POST"])
def content_one():
    """
    获取一条内容
    :return: settings-->RET
    """
    content_id = request.form.get("content_id")
    # 根据_id获取一条数据
    res = MONGO_DB.sources.find_one({"_id":ObjectId(content_id)})

    res["_id"] = str(res["_id"])  # 转换为str

    RET["code"] = 0
    RET["msg"] = ""
    RET["data"] = res

    return jsonify(RET)