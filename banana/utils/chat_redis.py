from setting import REDIS_DB
import json


def save_msg(sender, to_user):  # 保存消息
    # 1.查询一下xiao的Redis是否有数据
    user_msg_redis = REDIS_DB.get(to_user)
    if user_msg_redis:
        # 2.将xiao的数据反序列化成字典 { sender : n }
        user_msg_dict = json.loads(user_msg_redis)
        # 3.判断有没有 sender 的用户发来的消息数量
        if user_msg_dict.get(sender):
            # 数量加1
            user_msg_dict[sender] += 1
        else:
            # 第一次,初始值为1
            user_msg_dict[sender] = 1
    # 4.如果xiao是刚建立好的用户，他是没有消息的，字典是空
    else:
        user_msg_dict = {sender: 1}

    # 5.序列化用户消息字典user_msg_dict
    user_msg_redis = json.dumps(user_msg_dict)
    # 6.存回Redis
    REDIS_DB.set(to_user, user_msg_redis)

def get_msg_list(user):  # 获取消息
    user_msg_redis = REDIS_DB.get(user)
    if user_msg_redis:
        user_msg_dict = json.loads(user_msg_redis)
        # 统计数量
        user_msg_dict["count"] = sum(user_msg_dict.values())
    else:
        user_msg_dict = {"count":0}

    return user_msg_dict

def get_user_msg_one(sender, to_user):  # 获取用户一个好友消息
    user_msg_redis = REDIS_DB.get(to_user)
    if user_msg_redis:
        user_msg_dict = json.loads(user_msg_redis)
        if user_msg_dict.get(sender):
            return user_msg_dict.get(sender)
            # user_msg_dict[sender] = 0

    else:
        user_msg_dict = {sender:0}

    user_msg_redis = json.dumps(user_msg_dict)
    REDIS_DB.set(to_user,user_msg_redis)  # 修改redis