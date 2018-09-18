from flask import Flask, request,jsonify,render_template
from setting import MONGO_DB
from setting import RET
from bson import ObjectId
from serv import get_file
from serv import content
from serv import devices
from serv import toys

app = Flask(__name__)

app.register_blueprint(get_file.getfile)
app.register_blueprint(content.cont)
app.register_blueprint(devices.devs)
app.register_blueprint(toys.toy)

@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/login',methods=["POST"])
def login():
    """
    登陆验证
    :return: settings -> RET
    """
    try:
        RET["code"] = 1
        RET["msg"] = "用户名或密码错误"
        RET["data"] = {}

        username = request.form.get("username")
        password = request.form.get("password")

        user = MONGO_DB.users.find_one({"username": username, "password": password})

        if user:
            # 由于user中的_id是ObjectId对象,需要转化为字符串
            user["_id"] = str(user.get("_id"))
            RET["code"] = 0
            RET["msg"] = "欢迎登陆"
            RET["data"] = {"user_id": user.get("_id")}

    except Exception as e:
        RET["code"] = 1
        RET["msg"] = "登陆失败"

    return jsonify(RET)


@app.route('/reg',methods=["POST"])
def reg():
    """
    注册
    :return: {"code":0,"msg":"","data":""}
    """
    try:
        username = request.form.get("username")
        password = request.form.get("password")
        age = request.form.get("age")
        nickname = request.form.get("nickname")
        gender = request.form.get("gender")
        phone = request.form.get("phone")

        user_info = {
            "username": username,
            "password": password,
            "age": age,
            "nickname": nickname,
            # 判断gender==2,成立时为girl.jpg,否则为boy.jpg
            "avatar": "girl.jpg" if gender == 2 else "boy.jpg",
            "gender": gender,
            "phone": phone
        }

        res = MONGO_DB.users.insert_one(user_info)
        user_id = str(res.inserted_id)

        RET["code"] = 0
        RET["msg"] = "注册成功"
        RET["data"] = user_id
    except Exception as e:
        RET["code"] = 1
        RET["msg"] = "注册失败"

    return jsonify(RET)


@app.route('/user_info', methods=["POST"])
def user_info():
    user_id = request.form.get("user_id")

    # "password": 0 表示忽略密码字段
    res = MONGO_DB.users.find_one({"_id": ObjectId(user_id)}, {"password": 0})
    if res:
        res["_id"] = str(res.get("_id"))

    RET["code"] = 0
    RET["msg"] = ""
    RET["data"] = res

    return jsonify(res)

if __name__ == '__main__':
    app.run("0.0.0.0", 9527, debug=True)
