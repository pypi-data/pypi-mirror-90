from io import IOBase
import logging
import os
from typing import List
import zipfile
import shutil
from pathlib import Path
from hashlib import md5

import yaml
import re

from .api import Backend

DEFAULT_URL = 'http://kpl--backend.kpl.svc.cluster.local:8919/'
DEFAULT_LOCATE = '/kpl/user_keys/token.jwt'

logger = logging.getLogger("kpl-helper")

_backend_url = os.getenv(
    "KPL_BACKEND_HOST")
    
if not _backend_url:
    logger.warning("KPL_BACKEND_HOST not found, using default url: " + DEFAULT_URL)
    _backend_url = DEFAULT_URL
    
_token_locate = os.getenv(
    "KPL_TOKEN_LOCATE") or DEFAULT_LOCATE  # Token JWT

# Read jwt token inside container
_token = os.getenv("KPL_TOKEN")
if not _token:
    try:
        with open(_token_locate) as fd:
            _token = fd.read()
    except:
        logger.error("Cannot access server. No KPL_TOKEN or KPL_TOKEN_LOCATE env found.")
        exit(1)
    


class Uploader:
    """
    使用Backend API上传文件的包装类
    """

    def __init__(self, name: str, path: str):
        self.api = Backend(_backend_url, _token)
        self.name = name
        self.path = Path(path)
        self.operate_uuid = None
        self.preupload_id = None
        self.chunk_size = None
        self.savetype = None

    def upload_file(self, filename: str):
        """上传文件

        """
        with open(filename, 'rb') as upload_file:
            sz = os.path.getsize(filename)  # 获取文件大小

            self.md5 = self._get_file_md5(upload_file)  # 分片读取md5

            upload_file_name = filename  # 创建上传文件名

            self.preupload_id, self.chunk_size = \
                self.api.preupload(description="",
                                   filename=upload_file_name,
                                   name=self.name,
                                   type=self.savetype,
                                   md5=self.md5,
                                   size=sz)

            # 切换回头部，开始传输
            upload_file.seek(0)
            offset = 0
            while offset != sz:
                data = upload_file.read(self.chunk_size)
                data_len = len(data)

                # 判断是否为最后一片
                is_last = False
                if data_len + offset == sz:
                    is_last = True

                part_md5 = self._get_data_md5(data)
                self.api.upload(id=self.preupload_id,
                                chunk_offset=offset,
                                md5=self.md5,
                                is_last=is_last,
                                type=self.savetype,
                                file=data,
                                filename=filename
                                )
                offset += data_len

    def _gen_zip(self, pathlist: List[Path], zipname: str):
        """打包所有的文件到一个压缩包中
        """
        with zipfile.ZipFile(zipname, 'w') as z:
            for path in pathlist:
                z.write(path, arcname=path.relative_to(os.path.abspath(self.path.joinpath(".."))))

    def _check_dir(self):
        """检查目录是否存在"""
        if not self.path.exists():
            raise Exception("不存在该目录")

    def _check_name_existed(self, name) -> bool:
        raise NotImplementedError()

    def _find_available_name(self, name):
        """检查名称是否存在，如果存在自动加后缀“-1,2,3,4”"""
        origin_name = name
        suffix_num = 1
        while True:
            if self._check_name_existed(name):
                name = origin_name + '-' + str(suffix_num)
                suffix_num += 1
            else:
                break

        return name

    def _check_vaild_name(self, name):
        """只支持中英文、数字、中下划线"""
        for ch in name:
            if not (is_chinese_char(ch) or ch.isalnum() or ch in "_-"):
                raise Exception("名称只支持中英文、数字、中下划线")

    def _get_file_md5(self, fobj: IOBase, buff_len=8096 * 1024) -> str:
        """获得一个文件的md5值

        在文件过大时分片"""
        m = md5()
        while True:
            data_flow = fobj.read(buff_len)  # 每次读入8089kb进入内存
            if not data_flow:  # 读取完后返回空值，False
                break
            m.update(data_flow)

        return m.hexdigest()

    def _get_data_md5(self, buf: bytes) -> str:
        """获得一串字节的md5
        """
        m = md5()
        m.update(buf)
        return m.hexdigest()


class AlgorithmSaver(Uploader):
    """

    """
    MAX_ALG_FILE_SIZE = 50 * 1024 * 1024
    ENV_FILE_NAME = "environment.yml"

    def __init__(self, name, path):
        super().__init__(name, path)
        self.savetype = "algorithm"

    def save(self) -> str:
        self._check_dir()
        self._check_env_yaml()
        self.name = self._find_available_name(self.name)
        # 查找算法文件
        files = self._get_algorithm_files()
        # 判断文件大小
        self._check_file_size(files)

        zipname = self.name + "-" + self.savetype + "-save.zip"
        self._gen_zip(files, zipname)
        # 算法的上传方式是直接上传
        # TODO: 但是怎么判断算法的框架类型？
        with open(zipname, 'rb') as f:
            data = f.read()
            self.api.algorithm_create(
                name=self.name, framework_id=1, description="Added by kpl-helper", file=data)

        return self.name

    def _get_algorithm_files(self) -> List[Path]:
        """获取算法文件
        
        过滤掉.pyc文件和.git文件夹下的文件
        可能需要其他的过滤规则……
        """
        res: List[Path] = []
        for dirpath, _, filename in os.walk(self.path):
            res.extend([Path(os.path.join(dirpath, f)) for f in filename if not f.endswith(
                "pyc") and not ".git" in os.path.split(dirpath)])

        return res

    def _check_file_size(self, files: List[Path]):
        """检查所有算法文件的大小的和"""
        if sum([os.path.getsize(i) for i in files]) > self.MAX_ALG_FILE_SIZE:
            raise Exception("无法上传超过50MB的算法文件")

    def _check_name_existed(self, name) -> bool:
        """检查是否重名"""
        return self.api.algorithm_check_existed_name(name=name)

    def _check_env_yaml(self):
        """检查yaml格式是否正确"""

        yaml_file = self.path / self.ENV_FILE_NAME
        if not yaml_file.is_file():
            raise Exception("不是正确的算法格式，没有找到" + self.ENV_FILE_NAME + "文件")

        # 检查yaml文件是否有version、image两项
        with open(yaml_file) as f:
            y = yaml.load(f, Loader=yaml.FullLoader)
            if not all([i in y for i in ['version', 'image']]):
                raise Exception(self.ENV_FILE_NAME + "格式不正确")


class ModelSaver(Uploader):
    def __init__(self, name, path):
        super().__init__(name, path)
        self.savetype = "model"

    def _check_name_existed(self, name) -> bool:
        """检查是否重名"""
        return self.api.model_check_existed_name(name=name)

    def save(self) -> str:
        self._check_dir()
        # self._check_name_existed(self.name) # 该API还未实现

        zipname = self.name + "-" + self.savetype + "-save"
        if self.path.is_file():
            self.upload_file(str(self.path))
        else:
            shutil.make_archive(zipname, "zip", root_dir=os.path.abspath(self.path.joinpath("..")), base_dir=self.path)
            self.upload_file(zipname + ".zip")
        return self.name


class DatasetSaver(Uploader):
    def __init__(self, name, path):
        super().__init__(name, path)
        self.savetype = "dataset"

    def save(self) -> str:
        # 检查目录或文件是否存在
        # 判断是否为kpl-dataset格式
        self._check_dir()

        zipname = self.name + "-" + self.savetype + "-save"

        # 如果是kpl-dataset，压缩包就不含有子文件夹
        if self._check_if_kpl_dataset():
            shutil.make_archive(zipname, "zip", self.path, ".")
        else:
            shutil.make_archive(zipname, "zip", self.path)
        self.upload_file(zipname + ".zip")
        return self.name

    def _check_name_existed(self, name) -> bool:
        """检查是否重名"""
        return self.api.dataset_check_existed_name(name=name)

    def _check_if_kpl_dataset(self) -> bool:
        """检查是否是kpl-dataset

        如果同时包含 *.data和*.index则确定为kpl-dataset
        """
        kpl_dataset_globs = ['*.data', '*.index']
        if all([list(self.path.glob(fname)) for fname in kpl_dataset_globs]):
            return True


# 见：https://zhuanlan.zhihu.com/p/93029007
HAN_SCRIPT_PAT = re.compile(
    r'[\u4E00-\u9FEF\u3400-\u4DB5\u20000-\u2A6D6\u2A700-\u2B734'
    r'\u2B740-\u2B81D\u2D820-\u2CEA1\u2CEB0-\u2EBE0]'
)


def is_chinese_char(c):
    return bool(HAN_SCRIPT_PAT.match(c))
