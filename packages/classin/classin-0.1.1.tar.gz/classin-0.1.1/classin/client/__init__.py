# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging
import time
import hashlib

from six.moves.urllib_parse import urlparse, parse_qsl, urlencode

from . import api
from .base import BaseClient
from ..core.utils import to_binary

logger = logging.getLogger(__name__)


class ClassInClient(BaseClient):
    user = api.User()
    classroom = api.ClassRoom()
    school = api.School()
    group = api.Group()
    cloud = api.Cloud()
    broadcast = api.Broadcast()

    def __init__(self, sid, secret_key, api_base_url='https://api.eeo.cn/', timeout=None):
        super(ClassInClient, self).__init__(timeout)
        self.API_BASE_URL = api_base_url
        self.sid = sid
        self.secret_key = to_binary(secret_key)

    def get_sign(self, data):
        return hashlib.md5(self.secret_key + to_binary(data)).hexdigest().lower()

    def add_sign(self, data):
        data['SID'] = self.sid
        data['timeStamp'] = int(time.time())
        data['safeKey'] = self.get_sign(data['timeStamp'])
        return data

    def _handle_pre_request(self, method, uri, kwargs):
        if method == 'POST':
            data = kwargs.setdefault('data', dict())
            self.add_sign(data)
        return method, uri, kwargs

    def _handle_request_except(self, e, func, *args, **kwargs):
        raise e

    def check_sign(self, data, check_timestamp_second=300):
        """
        回调接口签名验证

        :param data: 请求全部数据
        :param check_timestamp_second: 时间戳与服务器时间误差范围，传0不验证时间戳
        """
        assert isinstance(data, dict)
        if 'SafeKey' not in data or 'TimeStamp' not in data:
            return False
        if data.get('SID', None) != self.sid:
            return False
        if check_timestamp_second > 0:
            if abs(data['TimeStamp'] - time.time()) > check_timestamp_second:
                return False
        data = data.copy()
        sign = data.pop('SafeKey', None)
        return sign == self.get_sign(data)

    def get_partner_url(
            self,
            account,
            nick_name,
            url,
            key,
            partner_url
    ):
        """
        免二次登陆地址
        https://docs.eeo.cn/api/zh-hans/broadcast/getWebcastUrl.html
        https://docs.eeo.cn/api/zh-hans/classroom/addCourseClass.html

        :param account: 账户
        :param nick_name: 昵称
        :param url: 通过接口获得播放器链接
        :param key: url签名参数名
        :param partner_url: url前缀
        """
        parsed_url = list(urlparse(url))
        parsed_qs = dict(parse_qsl(parsed_url[4]))
        parsed_qs['account'] = account
        parsed_qs['nickname'] = nick_name
        parsed_qs['checkCode '] = self.get_sign(parsed_qs[key] + account + nick_name)
        url = partner_url
        if '?' not in url:
            url += "?"
        if not url.endswith(("&", "?")):
            url += "&"
        url += urlencode(parsed_qs)
        return url
