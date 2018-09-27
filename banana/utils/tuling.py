import requests
import json
from setting import TL_URL as tuling_url
from setting import TL_DATA as data


def to_tuling(q,user_id):
    data["perception"]["inputText"]["text"] = q
    data["userInfo"]["userId"] = user_id
    res = requests.post(tuling_url, json=data)
    res_dic = json.loads(res.content.decode("utf8"))  # type:dict
    res_type = res_dic.get("results")[0].get("resultType")
    result = res_dic.get("results")[0].get("values").get(res_type)
    print(result)
    return result