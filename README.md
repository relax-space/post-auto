# bcp 工时
1. 配置环境变量
```bash

chromium_drive=C:\Users\Administrator\AppData\Local\pyppeteerpyppeteer\local-chromium\880765\chrome-win\chrome.exe

waitfortime=1000

post_host=https://www.360gkw.cc

post_dingtalk_url=https://oapi.dingtalk.com/robot/send?access_token=7d558c3e632a0f7e1120c550d127fa136aa41aa08fa7e73a7425b46e59c543b3

code_username=xxm

code_password=123

code_id=10001

```
2. pip install -r requirements.txt

3. 直接运行start.py即可

#docker 部署

### 方式1[`推荐`]：将chromium打包到镜像中，详情请看[dockerfile](Dockerfile)

# 最终业务

1. 同一个账号：2条/1小时
2. 帖子滚动发布


#更新记录

2021-06-05

同一个账号：2条/1小时