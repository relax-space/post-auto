import json
import os
from typing import List, Tuple


class File_:
    def __init__(self):
        pass

    @classmethod
    def get_ua_list(cls) -> List:
        return cls.read_list("relax/ua_fake.json")

    @classmethod
    def get_file_path(cls, directory: str, suffix: str = None) -> Tuple[List[str], str]:
        if not os.path.exists(directory):
            return None, 'directory is invalid:{0}'.format(directory)
        list = cls.get_file_path_pure(directory, suffix)
        return list, None

    @classmethod
    def get_file_path_pure(cls, directory: str, suffix: str = None) -> List[str]:
        list: List[str] = []
        files = os.listdir(directory)
        for file in files:
            m = os.path.join(directory, file)
            m = m.replace("\\", "/")
            if os.path.isfile(m):
                if (not suffix) or m.endswith(suffix):
                    list.append(m)
                    continue
        return list

    @classmethod
    def read_list(cls, path, mode="rt", encoding='utf-8', object_hook=None) -> List:
        ips = None
        with open(path, mode, encoding=encoding) as fp:
            if object_hook == None:
                ips = json.load(fp)
            else:
                ips = json.load(fp, object_hook=object_hook)
        return ips

    @classmethod
    def writeList(cls, list, dirPath, fileName, mode="w", encoding='utf-8', default=None, ensure_ascii=False):
        fileName = "%s/%s" % (dirPath, fileName)
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)
        with open(fileName, mode, encoding=encoding) as fp:
            if default == None:
                json.dump(list,
                          fp, ensure_ascii=ensure_ascii)
            else:
                json.dump(list,
                          fp, default=default, ensure_ascii=ensure_ascii)

    @classmethod
    def write(cls, contents, prePath, fileName, mode="w", encoding='utf-8'):
        cls.ensureDir(prePath)
        path = os.path.join(prePath, fileName).replace("\\", "/")
        with open(path, mode, encoding=encoding) as fp:
            fp.write(contents)

    @classmethod
    def read(cls, path, mode="rt", encoding='utf-8'):
        contents = []
        with open(path, mode, encoding=encoding) as fp:
            contents = fp.read()
        return contents

    @classmethod
    def ensureDir(cls, dirs):
        if not os.path.exists(dirs):
            os.makedirs(dirs)
