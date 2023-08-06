from typing import Tuple
import requests


class Backend:
    """
    KPL Backend
    """

    def __init__(self, url, jwt):
        if not jwt:
            raise Exception("jwt is necessary.")
        self.backend_url = url
        self.jwt = jwt
        self.sess = requests.session()
        self.post = self.wrap(self.sess.post)

    def wrap(self, func):
        """
        wrap for request header and response status code
        """

        def wrapped_http(url, **kwargs):
            kwargs["headers"] = {"authorization": self.jwt}
            kwargs["url"] = self.backend_url + url

            res = func(**kwargs)
            if not res.ok:
                raise Exception("网络错误", res.status_code)

            if res.json()['code'] != 'Success':
                raise Exception(res.json()['code'], res.json()['msg'])

            return res.json()['data']

        return wrapped_http

    def dataset_check_existed_name(self, **kwargs) -> bool:
        """
        POST application/json

        :param name: `str`
        :rtype: `bool` if the name existed
        """
        url = "api/v1/dev/dataset/check_existed_name"
        return self.post(url, json=kwargs)['existed']

    def model_check_existed_name(self, **kwargs) -> bool:
        """
        POST application/json

        :param name: `str`
        :rtype: `bool` if the name existed
        """
        url = "api/v1/dev/model/check_existed_name"
        return self.post(url, json=kwargs)['existed']

    def algorithm_check_existed_name(self, **kwargs) -> bool:
        """
        POST application/json

        :param name: `str`
        :rtype: `bool` if the name existed
        """
        url = "api/v1/dev/algorithm/check_existed_name"
        return self.post(url, json=kwargs)['existed']

    def preupload(self, **kwargs) -> Tuple[int, int]:
        """
        POST application/json

        :param description: `str` description of uploading object
        :param filename: `str` upload file name
        :param md5: `str`
        :param name: `str`
        :param size: `int` file size(bytes)
        :param type: `int` one of {"model", "algorithm", "dataset"}
        :rtype: `Tuple[int, int]` id for upload, chunk_size: size of single chunk, default=10Mb
        """
        url = "api/v1/dev/preupload"
        res = self.post(url, json=kwargs)
        return int(res["id"]), int(res["chunk_size"])

    def upload(self, **kwargs) -> None:
        """
        POST form

        :param id: `int` result of preupload
        :param chunk_offset: `int` description of uploading 
        :param md5: `str` this chunk checksum
        :param is_last: `bool` if this chunk is the last one 
        :param type: `str` one of {"model", "algorithm", "dataset"}
        :param file: `bytes` binary file content
        :param filename: `str`
        """
        url = "api/v1/dev/upload"
        self.post(url, files={
            "id": (None, kwargs['id']),
            "chunk_offset": (None, kwargs['chunk_offset']),
            "type": (None, kwargs['type']),
            "md5": (None, kwargs['md5']),
            "is_last": (None, kwargs['is_last']),
            "file": (kwargs['filename'], kwargs['file'], "application/octet-stream"),
        })

    def algorithm_create(self, **kwargs) -> None:
        """
        POST form

        :param name:
        :param description(optional):
        :param tag_ids(optional):
        :param framework_id:
        :param file:
        """
        url = "api/v1/dev/algorithm/create"
        files = {
            "name": (None, kwargs['name']),
            "description": (None, kwargs['description']),
            "framework_id": (None, kwargs['framework_id']),
            "file": ('algorithm.zip', kwargs['file'], "application/zip"),
        }

        self.post(url, files=files)
