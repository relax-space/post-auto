import asyncio
import datetime
import logging
import os
import random
import traceback
from typing import List

from async_retrying import retry
from pyppeteer import launch

from post.post import Post
from post.post_dto import PostDto
from post.settings_dto import SettingsDto
from post.user_dto import UserDto
from relax import File_, TimeZoneChina


async def page_evaluate(page):
    # 替换淘宝在检测浏览时采集的一些参数
    await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
    await page.evaluate('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')


def choice(posts: List[PostDto], now: datetime) -> PostDto:
    '''
    取出第一个，并放到最后
    '''
    post_dto = posts.pop(0)
    posts.append(post_dto)
    File_.writeList(
        posts, 'data', f'post{now.hour}.json', default=PostDto.to_dict)
    # post_dto.title = TimeZoneChina.format(now, '%Y%d%H%M%m')+' '+post_dto.title
    return post_dto


def get_users():
    '''
    每天移动一次用户的顺序
    '''
    users: List[UserDto] = File_.read_list(
        "data/user.json", object_hook=UserDto.from_dict)
    now = TimeZoneChina.now()
    weekday = now.isoweekday()
    if weekday == 1:
        return users
    elif weekday == 2:
        user_dto = users.pop(0)
        users.append(user_dto)
        return users
    elif weekday == 3:
        user_dto = users.pop(0)
        users.append(user_dto)
        user_dto = users.pop(0)
        users.append(user_dto)
        return users
    elif weekday == 4:
        user_dto = users.pop(0)
        users.append(user_dto)
        user_dto = users.pop(0)
        users.append(user_dto)
        user_dto = users.pop(0)
        users.append(user_dto)
        return users
    elif weekday == 5:
        user_dto = users.pop(0)
        users.append(user_dto)
        user_dto = users.pop(0)
        users.append(user_dto)
        user_dto = users.pop(0)
        users.append(user_dto)
        user_dto = users.pop(0)
        users.append(user_dto)
        return users


@retry(attempts=3)
async def login(settings_dto: SettingsDto, user_dto: UserDto, page):
    await asyncio.gather(
        page.goto(f'{settings_dto.post_host}/login/index.html'),
        page.waitForNavigation(),
    )
    # 选中输入框
    element = await page.J('#user_name')
    await page.waitFor(settings_dto.waitfortime)
    # 获取内容
    input_text = await (await element.getProperty('value')).jsonValue()
    if input_text:
        # 删除输入框里的内容
        await element.click({'clickCount': 3})  # 单击输入框三次选中
    # 清空输入框里的内容
    await page.waitFor(settings_dto.waitfortime)
    # 输入用户名，密码
    # delay是限制输入的时间
    post = Post()
    await page.type('#user_name', user_dto.user_name, {'delay': post.input_time_random() - 50})
    await page.type('#password1', user_dto.password, {'delay': post.input_time_random()})
    page.mouse
    # 点击提交，并等待页面正确响应。
    await asyncio.gather(
        page.click("#sub_login > p:nth-child(7) > input"),
        page.waitForNavigation(),
    )
    await page.waitFor(settings_dto.waitfortime)


async def logout(waitfortime: int, page):
    await page.click('#login_status > li:nth-child(4) > a')
    await page.waitFor(waitfortime+5000)


async def post(settings_dto: SettingsDto):
    now = TimeZoneChina.now()
    if now.hour < 7 or now.hour > 18:
        return
    try:
        # 'headless': False如果想要浏览器隐藏更改False为True
        print('进来了')
        browser = None
        if not settings_dto.chromium_drive:
            browser = await launch({
                'headless': True,
                'args': ['--no-sandbox',
                         '--disable-gpu'],
                'dumpio': True})
        else:
            browser = await launch({
                'headless': True,
                'executablePath': settings_dto.chromium_drive,
                'args': ['--no-sandbox',
                         '--disable-gpu'],
                'dumpio': True})
        # hourCalc = HourCalc(host)

        context = await browser.createIncognitoBrowserContext()  # 开启无痕浏览器模式
        page = await context.newPage()
        await page.setViewport({'width': 1920, 'height': 1080})
        ua = random.choice(File_.get_ua_list())
        await page.setUserAgent(ua)
        # login
        diff_days = (datetime.datetime.now() -
                     datetime.datetime(2021, 6, 18)).days
        now = TimeZoneChina.now()
        hour = now.hour
        users: List[UserDto] = get_users()
        posts: List[PostDto] = File_.read_list(
            f"data/post{hour}.json", object_hook=PostDto.from_dict)
        post = Post()
        for user_dto in users:
            await login(settings_dto, user_dto, page)
            # 第1次/1小时
            post_dto = choice(posts, now)
            temp = post_dto.title
            post_dto.title = f'{temp}{diff_days}'
            await post.send(settings_dto, user_dto, post_dto, ua, page)
            post_dto.title = temp
            # 第2次/1小时
            post_dto = choice(posts, now)
            temp = post_dto.title
            post_dto.title = f'{temp}{diff_days}'
            await post.send(settings_dto, user_dto, post_dto, ua, page)
            post_dto.title = temp
            await logout(waitfortime, page)

    except Exception as e:
        logging.error(f'exception:{traceback.format_exc()}')
        raise e
    finally:
        await page.close()
        await context.close()
        await browser.close()

    pass


if __name__ == '__main__':
    try:
        logging.basicConfig(level=logging.INFO,
                            format="%(asctime)s - %(levelname)s - %(message)s")
        chromium_drive = os.getenv('chromium_drive')
        waitfortime = 2000 if not os.getenv(
            'waitfortime') else int(os.getenv('waitfortime'))
        post_host = os.environ['post_host']
        dingtalk_url = os.environ['post_dingtalk_url']
        code_username = os.environ['code_username']
        code_password = os.environ['code_password']
        code_id = os.environ['code_id']
        settings_dto = SettingsDto(chromium_drive, waitfortime, post_host,
                                   dingtalk_url, code_username, code_password, code_id)
        task = asyncio.get_event_loop().run_until_complete(
            post(settings_dto))
        print(task)
    except Exception as e:
        logging.error(f'exception:{traceback.format_exc()}')
