import mimetypes
import smtplib
from email.header import Header
from email.message import EmailMessage
from typing import List

from click import echo, style

from relax.api_request import Requester


def send_email(server, email, password, to_list: str, subject, content, attach_path):
    """
    发送邮件
    :param server:邮件服务器
    :param email: 发送者邮件地址
    :param password: 邮箱密码
    :param to_list: 发送地址列表,多个用逗号隔开
    :param subject: 主题
    :param content: 发送邮件内容
    :param attach_path: 发送邮件附件
    :param debug_level: 发送邮件debug级别,默认为0
    """
    msg = EmailMessage()
    msg['From'] = email
    msg['To'] = to_list
    msg['Subject'] = Header(subject, 'utf-8').encode()
    msg.set_content(content, subtype='html', charset='utf-8', cte='8bit')

    ctype, encoding = mimetypes.guess_type(attach_path)
    if ctype is None or encoding is not None:
        # No guess could be made, or the file is encoded (compressed), so
        # use a generic bag-of-bits type.
        ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    with open(attach_path, 'rb') as fp:
        msg.add_attachment(fp.read(), maintype, subtype, filename=attach_path)
    with smtplib.SMTP_SSL(server) as smtp:
        # HELO向服务器标志用户身份
        smtp.ehlo_or_helo_if_needed()
        # 登录邮箱服务器
        smtp.login(email, password)
        smtp.send_message(msg)


def send_ding_talk_msg(hook_url: str, report_url: str, mobiles: List[str], msg: str, isAtAll: bool):
    """
    发送钉钉消息
    :param project_name: 项目名称
    :param hook_url: 回调地址
    :param test_result: 测试结果
    """
    pass_pic_url = "https://s1.ax1x.com/2020/06/25/NwjUG6.png"
    fail_pic_url = "https://s1.ax1x.com/2020/06/27/NyoprQ.png"
    msg = {
        "msgtype": "text",
        "text": {
            "content": f'\n{msg}\n{report_url}\n',
        },
        "at": {
            "atMobiles": mobiles,
            "isAtAll": isAtAll
        },
    }
    kwargs = {
        "url": hook_url,
        "json": msg,
        "method": "post",
    }
    res = Requester(kwargs).do().json()
    if res['errcode'] > 0:
        echo(style('发送钉钉消息失败，[%s]，请检查后重试' % res['errmsg'], fg='red'))
        return
    echo(style('钉钉消息发送成功，请查收', fg='green'))
