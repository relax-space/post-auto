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
        detail = "深圳市星辰信息服务有限公司合作流程： \n1、费用一次付清 \n2、职称只用于资质升级和年检 \n3、职称不得用于招投标活动，自己要求挂项目的除外 \n4、妥善保管工程师原件及其他有关材料 \n\n有讠正人才请通过以下方式联系 \n联系人：王工 \n微信：147-7496-9229 \n电话：147-7496-9229 \n在线扣扣：2853-0125-34 \n微信扫一扫，及时了解投递状态"

        await page.type('#detail_info', detail)

        code = Code()
        v_code = await code.fetch_captcha(settings_dto, ua, page)
        await page.type('#check_code', v_code, {'delay': self.input_time_random()})

        # 点击发布，并等待页面正确响应。
        await page.click("#sub_hunt_post")

        msg = f'职位标题:{post_dto.title}\n'

        msg += f'360账号:{user_dto.user_name}\n\n'

        send_ding_talk_msg(
            settings_dto.dingtalk_url,
            f"",
            [], msg, False)

        pass
