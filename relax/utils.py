import json
import logging
import math
import os
import re
import traceback
import uuid
from string import Formatter
from typing import Dict, List, OrderedDict, Union

import requests
from PIL import Image
from requests.cookies import RequestsCookieJar

from relax.consts import PROJECT_DIR_FLAG_FILE_NAME


def valid_captcha(raw: str) -> bool:
    if (not raw) or (len(raw) != 4):
        return False
    result = re.findall(r'[0-9a-zA-Z]+', raw)
    value = ''.join(result)
    if len(value) != 4:
        return False
    return True


def cookies_to_dict(cookies: RequestsCookieJar) -> Dict:
    return requests.utils.dict_from_cookiejar(cookies)


def dict_to_cookies(cookies_dict: Dict) -> RequestsCookieJar:
    return requests.utils.cookiejar_from_dict(cookies_dict)


def regex_en(raw: str):
    result = re.findall(r'[a-zA-Z]+', raw)
    return ''.join(result)


def regex_en_upper(raw: str):
    result = re.findall(r'[A-Z]+', raw)
    return ''.join(result)


def regex_zh(raw: str):
    result = re.findall(r'[\u4e00-\u9fa5]+', raw)
    return ''.join(result)


def split(raw_list: List, group_count: int) -> List[List]:
    """
    group_count =2 
    [1,2,3,4,5,6,7] ==> [[1,2,3,4],[,5,6,7]]
    """
    # 大列表中几个数据组成一个小列表
    count = len(raw_list)
    n = math.ceil(count/group_count)
    return [raw_list[i:i + n] for i in range(0, count, n)]


def split_content(raw_list: List, content_count: int) -> List[List]:
    """
    content_count =2
    [1,2,3,4,5,6,7] ==> [[1,2],[3,4],[5,6],[7]]
    """
    # 大列表中几个数据组成一个小列表
    count = len(raw_list)
    n = content_count
    return [raw_list[i:i + n] for i in range(0, count, n)]


def get_uuid() -> int:
    return uuid.uuid4().int


def get_format_params(format_str: str) -> List[str]:
    return [fname for _, fname, _, _ in Formatter().parse(format_str) if fname]


def eq_list(list1: list, list2: list) -> bool:
    return sorted(list1) == sorted(list2)


def is_subset(subset: Dict, superset: Dict) -> bool:
    if isinstance(subset, dict):
        return all(key in superset and is_subset(val, superset[key]) for key, val in subset.items())

    if isinstance(subset, list) or isinstance(subset, set):
        return all(any(is_subset(subitem, superitem) for superitem in superset) for subitem in subset)

    # assume that subset is a plain value if none of the above match
    return subset == superset


def reverse_dict(raw_dict: Dict[str, str]) -> Dict:
    return {v: k for k, v in raw_dict.items()}


def check_json(content: str) -> bool:
    try:
        json.loads(content)
        return True
    except Exception as e:
        logging.error(f'raw data:{content},exception:{traceback.format_exc()}')
        return False


def check_form(content: str) -> bool:
    return check_json(content)


def get_json(content: Union[str, bytes]) -> dict:
    if not content:
        return None
    if isinstance(content, (str, bytes)):
        try:
            content = json.loads(content)
        except Exception as e:
            logging.error(
                f'raw content:{content},exception:{traceback.format_exc()}')
            content = None
        finally:
            return content
    return None


def format_json(content):
    if isinstance(content, (str, bytes)):
        try:
            return json.loads(content)
        except:
            return content
    return content


def get_project_dir():
    return get_root_dir(
        PROJECT_DIR_FLAG_FILE_NAME, os.getcwd())


def get_root_dir(flag_file_name, cur_dir):
    if os.path.isfile(cur_dir):
        cur_dir = os.path.dirname(cur_dir)
    if flag_file_name in os.listdir(cur_dir):
        return cur_dir

    up_dir = os.path.dirname(cur_dir)
    if up_dir == cur_dir:
        return None
    return get_root_dir(flag_file_name, up_dir)


def str_to_dict(contents, sep1=",", sep2="=") -> Dict:
    dict: Dict = {}
    lines = contents.strip().split(sep1)
    value = None
    for line in lines:
        ln = line.strip()
        if len(ln) == 0:
            continue
        index = ln.find(sep2)
        if index == -1:
            return None
        value = ln[index+1:]
        dict[ln[:index]] = int(value) if str.isdigit(value) else value
    return dict


class ConfigFileParser:
    def __init__(self, suffix, file_path):
        if not isinstance(file_path, str):
            raise ValueError('file_path error, is not a valid str')

        if not os.path.isfile(file_path):
            raise ValueError('file_path error, is not a valid file path')

        self.file_path = file_path
        self.content = None
        self.parser = self.get_parser(suffix)

        try:
            with open(self.file_path, encoding='utf-8') as f:
                self.content = self.parser(f) or {}
        except Exception:
            logging.error(
                f'raw file_path:{file_path},exception:{traceback.format_exc()}')
            raise ValueError('%s is not a valid %s file' % (file_path, suffix))

    @staticmethod
    def get_parser(suffix):
        if suffix == 'json':
            return json.load
        else:
            raise ValueError('不支持的配置文件类型')

    def as_dict(self):
        return self.content


def fixation_order(d):
    """
    固定参数顺序，以防在传参过程中变掉，导致验签等失败
    """
    o = OrderedDict()
    for i in d:
        if not d[i]:
            continue
        o[i] = d[i]
    return o


project_dir = get_project_dir()
