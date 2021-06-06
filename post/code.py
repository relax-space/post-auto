import logging
from hashlib import md5
from typing import Dict, Tuple

import requests
from PIL import Image
from relax import valid_captcha
from relax.utils import format_json
from requests.models import Response

from post.settings_dto import SettingsDto


class Code:
    def __init__(self):
        self.captcha_image_tag = '#form_hunt_post > p:nth-child(15) > span.hunt-name-span > img'
        pass

    async def get_captcha_image(self, page) -> Image:
        captcha = await page.waitForSelector(self.captcha_image_tag)
        await captcha.screenshot({'path': 'captcha.png'})
        return open('captcha.png', 'rb').read()

    async def fetch_captcha(self, settings_dto: SettingsDto,  ua: str, page) -> str:
        image = await self.get_captcha_image(page)
        code, pid = self.post_captcha(settings_dto, image, ua)
        logging.info(f'code {code}, pid {pid}')
        index = 0
        while index < 3:
            index = index+1
            if not self.valid_captcha2(code, settings_dto, pid, ua):
                await page.click(self.captcha_image_tag)
                await page.waitFor(settings_dto.waitfortime + 5000)
                code, pid = self.post_captcha(settings_dto, image, ua)
                logging.info(f'code {code}, pid {pid}')
                continue
            logging.info("识别成功")
            break
        if not valid_captcha(code):
            raise RuntimeError(f'重试了3次，验证码依然不对')
        return code

    def valid_captcha2(self, code: str, settings_dto: SettingsDto, pid: str, ua: str) -> str:
        new_code = valid_captcha(code)
        if not new_code:
            logging.info(f'验证码失败 code:{code},new_code:{new_code} pid:{pid}')
            resp = self.report_error_captcha_pure(settings_dto, pid, ua)
            logging.error(f'报告验证码，{self._log(resp)}')
        return new_code

    def _log(self, resp: Response) -> str:
        return f'url: {resp.url}, data: {format_json(resp.request.body)}, status_code: {resp.status_code}, resp_raw: {resp.json()}'

    def post_captcha(self, settings_dto: SettingsDto, image: Image, ua: str) -> Tuple[str, str]:
        # {'err_no': 0, 'err_str': 'OK', 'pic_id': '1143319066445800003', 'pic_str': '7261', 'md5': 'f25c730b34e2ca840cda96047833de3d'}
        resp = self.post_captcha_pure(settings_dto, image, ua)
        logging.error(f'请求验证码，{self._log(resp)}')
        if resp.status_code != 200:
            logging.error(f'请求验证码错误，响应状态不是200')
            return '', ''
        resp_dict: Dict = resp.json()
        return resp_dict.get('pic_str', ''), resp_dict.get('pic_id', '')

    def post_captcha_pure(self, settings_dto: SettingsDto, image: Image, ua: str) -> Response:
        """
        识别验证码
        """
        password = settings_dto.code_password.encode('utf8')
        password = md5(password).hexdigest()
        kwargs = {
            'headers': {
                'Connection': 'Keep-Alive',
                'User-Agent': ua,
            },
            'method': 'POST',
            'url': 'http://upload.chaojiying.net/Upload/Processing.php',
            'data': {
                'user': settings_dto.code_username,
                'pass2': password,
                'softid': settings_dto.code_id,
                'codetype': 1004,
            },
            'files': {
                'userfile': ('captcha.png', image)
            }
        }
        resp = requests.post('http://upload.chaojiying.net/Upload/Processing.php',
                             data=kwargs.get('data'), files=kwargs.get('files'), headers=kwargs.get('headers'))
        return resp

    def report_error_captcha_pure(self, settings_dto: SettingsDto, pid: str, ua: str) -> Response:
        """
        识别验证码
        """
        password = settings_dto.code_password.encode('utf8')
        password = md5(password).hexdigest()
        kwargs = {
            'headers': {
                'User-Agent': ua
            },
            'method': 'POST',
            'url': 'http://upload.chaojiying.net/Upload/ReportError.php',
            'data': {
                'user': settings_dto.code_username,
                'pass2': password,
                'softid': settings_dto.code_id,
                'id': pid,
            },
        }
        resp = requests.post('http://upload.chaojiying.net/Upload/ReportError.php',
                             data=kwargs.get('data'), headers=kwargs.get('headers'))
        return resp
