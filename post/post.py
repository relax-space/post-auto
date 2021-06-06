import asyncio
import random

from relax import send_ding_talk_msg

from post.code import Code
from post.post_dto import PostDto
from post.settings_dto import SettingsDto
from post.user_dto import UserDto
from post.util import getValueByText


class Post:
    def __init__(self):
        pass

    def input_time_random(self):
        return random.randint(100, 151)

    async def select(self, select_tag: str, text: str, page):
        value = await getValueByText(text, select_tag, page)
        await page.select(select_tag, value)

    async def radio(self, tag: str, text: str, page):
        for current_tag in await page.querySelectorAll(tag):
            tag_text = await page.evaluate('e => e.innerText', current_tag)
            if tag_text == text:
                await current_tag.click()
                break

    async def send(self, settings_dto: SettingsDto, user_dto: UserDto, post_dto: PostDto, ua: str, page):
        # 进入个人首页
        await asyncio.gather(
            page.goto(f'{settings_dto.post_host}/Hunt/index.html'),
            page.waitForNavigation(),
        )
        # 点击发布职位
        await asyncio.gather(
            page.click(
                "#div1 > div > div.hunt-resource-management > p.hunt-release > a:nth-child(2)"),
            page.waitForNavigation(),
        )
        # 选择分类
        for class1Tag in await page.querySelectorAll(f'#tab2 > ul > li > div'):
            class1 = await page.evaluate('e => e.innerText', class1Tag)
            if class1 == post_dto.class1:
                await class1Tag.click()
                await page.waitFor(settings_dto.waitfortime)
                for class2Tag in await class1Tag.querySelectorAll(f'ul > li > a'):
                    class2 = await page.evaluate('e => e.innerText', class2Tag)
                    if class2 == post_dto.class2:
                        await class2Tag.click()
                        await page.waitFor(settings_dto.waitfortime)
                        break
                break
        await page.type('#pos_name', post_dto.title, {'delay': self.input_time_random()})
        await self.select('#province_pos', post_dto.province, page)
        await page.waitFor(settings_dto.waitfortime)
        await self.select('#city_pos', post_dto.city, page)
        await self.select('#edu', post_dto.edu, page)
        await self.radio('#form_hunt_post > p:nth-child(7) > label', post_dto.method, page)
        await self.radio('#form_hunt_post > p:nth-child(8) > label', post_dto.work_type, page)
        await self.radio('#form_hunt_post > p:nth-child(9) > label', post_dto.reg_status, page)
        await self.radio('#form_hunt_post > p:nth-child(10) > label', post_dto.degree_level, page)
        await self.radio('#form_hunt_post > p:nth-child(11) > label', post_dto.cert_use, page)

        await self.select('#expect_pay', post_dto.expect_pay, page)
        await self.select('#expect_pay_time', post_dto.expect_pay_time, page)

        await self.radio('#form_hunt_post > p:nth-child(13) > label', post_dto.yeji_needs, page)

        await page.type('#detail_info', post_dto.detail_info)

        code = Code()
        v_code = await code.fetch_captcha(settings_dto, ua, page)
        await page.type('#check_code', v_code, {'delay': self.input_time_random()})

        # 点击发布，并等待页面正确响应。
        await page.click("#sub_hunt_post")

        msg = f'360账号:{user_dto.user_name}\n\n'

        msg += f'{post_dto.class1}({post_dto.class2})\n'

        msg += f'职位标题:{post_dto.title}\n'
        msg += f'用证地区:{post_dto.province} {post_dto.city}\n'
        msg += f'学历要求:{post_dto.edu}\n'
        msg += f'签约方式:{post_dto.method}\n'
        msg += f'工作性质:{post_dto.work_type}\n'

        msg += f'注册情况:{post_dto.reg_status}\n'
        msg += f'职    称:{post_dto.degree_level}\n'
        msg += f'证书用途:{post_dto.cert_use}\n'
        msg += f'职位薪资:{post_dto.expect_pay}/{post_dto.expect_pay_time}\n'
        msg += f'业绩要求:{post_dto.yeji_needs}\n'

        msg += f'详细说明:{post_dto.detail_info}\n'

        send_ding_talk_msg(
            settings_dto.dingtalk_url,
            f"",
            [], msg, False)

        pass
