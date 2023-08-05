# encoding: utf-8
from __future__ import absolute_import, unicode_literals

from optionaldict import optionaldict

from .base import BaseAPI


class Group(BaseAPI):
    """
    班级群相关接口
    https://docs.eeo.cn/api/zh-hans/group/
    """

    def modifyGroupMemberNickname(
            self,
            course_id,
    ):
        """
        修改群成员的班级昵称
        https://docs.eeo.cn/api/zh-hans/group/modifyGroupMemberNickname.html

        :param course_id: 课程 ID
        """
        return self._post(
            params={'action': 'modifyGroupMemberNickname'},
            data=optionaldict({
                'courseId': course_id,
            }),
        )
