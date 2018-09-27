## 说明
智能玩具，采用html5+和Flask

## 文件说明

| filename | describe |
|---------|--------|
| MyApp          | HBuilder项目 |
| banana          | Flask项目 |
| MongoDB          | MongoDB相关表 |
| adb.bat          | HBuilder连接夜神模拟器，注意修改路径！ |

注意：adb.bat要修改一下部分：

`cd D:\Program Files\Nox\bin`

`D:`

`cd D:\Program Files (x86)\HBuilder.9.1.13.windows\HBuilder\tools\adbs`

请确保 adb.bat和HBuilder，夜神模拟器在同一个盘符下，比如D盘！

## 项目结构
```
./
├── audio  # 音频文件以及提示语
├── audio_img  # 音频文件对应的图片
├── chat  # 聊天语言文件
├── device_code  # 玩具设备二维码,uuid4+时间戳生成的
├── im_serv.py  # websocket服务
├── manager.py  # App 后端接口
├── QRcode.py  # 生成二维码图片
├── serv  # 蓝图
│   ├── chat.py  # 聊天相关接口
│   ├── content.py  # 内容相关接口
│   ├── devices.py  # 设备相关接口
│   ├── friend.py  # 好友相关接口
│   ├── get_file.py  # 文件相关接口
│   └── toys.py  # 玩具相关接口
├── setting.py  # 配置文件
├── static  # 静态目录
│   ├── jquery.min.js
│   └── recorder.js
├── templates  # 模板
│   └── index.html
├── utils  # 工具
│   ├── baidu_ai.py  # 百度AI
│   ├── chat_redis.py  # 连接redis,用来存储App消息通知
│   ├── fenci.py  # 分词测试
│   ├── lowB_plus.py  # 集成jieba gensim pypinyin
│   └── tuling.py  # 图灵
└── xiaopapa.py  # 爬虫
```

## 运行环境

| Project | version | Description |
|---------|--------|-------------|
| python          | 3.6.5 | 在这个版本以及以上都可以 |
| Flask                | 1.0.2 | 无 |
| HBuilder                | 1.0.2 | 无 |
| MongoDB                | 3.4 | 库名为bananabase |
| 夜神模拟器                | 6.2.1.1 | 无 |
| Redis                | 3.2.10 | 无 |

## 功能

| 路径 | 功能 | 说明 |
|---------|--------|-------------|
| /       | 首页 | GET |
| /login/ | 登录 | POST |
| /reg/   | 注册 | POST |
| /user_info/ | 用户信息 | POST |
| /get_audio/ | 获取音频 | GET |
| /get_image/ | 获取图片 | GET |
| /content_list/ | 内容列表 | POST |
| /content_one/ | 获取一条内容 | POST |
| /yanzheng_qr/ | 验证二维码 | POST |
| /bind_toy/ | 绑定玩具 | POST |
| /toy_list/ | 玩具列表 | POST |
| /device_toy_id/ | 验证设备id | POST |
| /chat_list/ | 聊天记录列表 | POST |
| /get_msg/ | 获取聊天语言文件 | POST |
| /get_msg_list/ | 获取角标 | POST |
| /friend_list/ |  好友列表 | POST |
| /add_req/ |   添加好友请求 | POST |
| /req_list/ |   添加请求列表 | POST |
| /get_req/ |  获取一个好友请求 | POST |
| /acc_req/ |  允许一个好友请求 | POST |
| /ref_req/ |  拒绝一个好友请求 | POST |

## 运行方式

| Project | Description |
|---------|--------|
| Flask | 打开项目banana,运行`manager.py` |
| HBuilder | 打开项目MyApp |
| MongoDB | 执行命令`mongod` |
| 夜神模拟器 | 最后启动,并执行`adb.bat` |


## 导出表
`mongoimport --db bananabase --collection chat --file chat.json --type json`

`mongoimport --db bananabase --collection devices --file devices.json --type json`

`mongoimport --db bananabase --collection req --file req.json --type json`

`mongoimport --db bananabase --collection sources --file sources.json --type json`

`mongoimport --db bananabase --collection toys --file toys.json --type json`

`mongoimport --db bananabase --collection users --file users.json --type json`


## 导出表

`mongoexport -d bananabase -c chat --type=json -f _id,user_list -o E:/git/Intelligent_toy/MongoDB/chat.json`

`mongoexport -d bananabase -c devices --type=json -f _id,device_id -o E:/git/Intelligent_toy/MongoDB/devices.json`

`mongoexport -d bananabase -c req --type=json -f _id,req_user,req_type,req_toy,req_msg,avatar,user_remark,user_nick,status -o E:/git/Intelligent_toy/MongoDB/req.json`

`mongoexport -d bananabase -c sources --type=json -f _id,title,nickname,avatar,audio,avatar,intro,category,play_count -o E:/git/Intelligent_toy/MongoDB/sources.json`

`mongoexport -d bananabase -c toys --type=json -f _id,device_id,toy_name,baby_name,gender,avatar,bind_user,friend_list -o E:/git/Intelligent_toy/MongoDB/toys.json`

`mongoexport -d bananabase -c users --type=json -f _id,username,password,age,nickname,gender,phone,avatar,bind_toy,friend_list -o E:/git/Intelligent_toy/MongoDB/users.json`



## 效果
首页：

![Image text](https://github.com/987334176/Intelligent_toy/blob/master/%E6%95%88%E6%9E%9C%E5%9B%BE/%E9%A6%96%E9%A1%B5.png)

登录：

![Image text](https://github.com/987334176/Intelligent_toy/blob/master/%E6%95%88%E6%9E%9C%E5%9B%BE/%E7%99%BB%E5%BD%95.png)

注册：

![Image text](https://github.com/987334176/Intelligent_toy/blob/master/%E6%95%88%E6%9E%9C%E5%9B%BE/%E7%94%A8%E6%88%B7%E6%B3%A8%E5%86%8C.png)

聊天：

![Image text](https://github.com/987334176/Intelligent_toy/blob/master/%E6%95%88%E6%9E%9C%E5%9B%BE/%E8%81%8A%E5%A4%A9.png)

玩具详情：

![Image text](https://github.com/987334176/Intelligent_toy/blob/master/%E6%95%88%E6%9E%9C%E5%9B%BE/%E7%8E%A9%E5%85%B7%E8%AF%A6%E6%83%85.png)


Copyright (c) 2018-present, xiao You