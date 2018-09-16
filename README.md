## 说明
智能玩具，采用html5+和Flask

## 文件说明

| filename | describe |
|---------|--------|
| MyApp          | HBuilder项目 |
| banana          | Flask项目 |
| sources.json          | MongoDB表sources |
| users.json          | MongoDB表users |
| adb.bat          | HBuilder连接夜神模拟器，注意修改路径！ |

注意：adb.bat要修改一下部分：

`cd D:\Program Files\Nox\bin`

`D:`

`cd D:\Program Files (x86)\HBuilder.9.1.13.windows\HBuilder\tools\adbs`

请确保 adb.bat和HBuilder，夜神模拟器在同一个盘符下，比如D盘！

## 运行环境

| Project | version | Description |
|---------|--------|-------------|
| python          | 3.6.5 | 在这个版本以及以上都可以 |
| Flask                | 1.0.2 | 无 |
| HBuilder                | 1.0.2 | 无 |
| MongoDB                | 3.4 | 库名为bananabase |
| 夜神模拟器                | 6.2.1.1 | 无 |

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

## 运行方式

| Project | Description |
|---------|--------|
| Flask | 打开项目banana,运行`manager.py` |
| HBuilder | 打开项目MyApp |
| MongoDB | 执行命令`mongod` |
| 夜神模拟器 | 最后启动,并执行`adb.bat` |


## 效果
首页：



Copyright (c) 2018-present, xiao You