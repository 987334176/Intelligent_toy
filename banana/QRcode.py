from uuid import uuid4
import hashlib, time,os
import requests
import setting

def create_device_id(count=1):
    device_list = []
    for i in range(count):

        # 生成唯一设备id,f-string是Python 3.6语法
        device_id = f"{uuid4()}{time.time()}"
        device_id_md5 = hashlib.md5(device_id.encode("utf8"))  # 生成md5对象

        qr_code = device_id_md5.hexdigest()  # 获取md5的值
        qr_url = f"{setting.CREATE_QR_URL}{qr_code}"  # 生成二维码访问链接
        res = requests.get(qr_url)  # 使用GET请求
        # 拼接二维码图片保存路径
        code_file = os.path.join(setting.DEVICE_CODE_PATH,f"{qr_code}.jpg")

        with open(code_file, "wb") as f:
            f.write(res.content)  # 写入文件

        device_list.append({"device_id": qr_code})  # 追加到列表中

        time.sleep(0.2)  # 睡眠0.2秒,防止被封锁IP

    setting.MONGO_DB.devices.insert_many(device_list)  # 写入多条记录


create_device_id(5)  # 生成5条记录