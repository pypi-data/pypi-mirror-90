# encoding: utf-8
from __future__ import absolute_import, unicode_literals

from optionaldict import optionaldict

from .base import BaseAPI


class School(BaseAPI):
    """
    机构相关接口
    https://docs.eeo.cn/api/zh-hans/school/
    """

    def add_school_label(
            self,
            label_name,
    ):
        """
        添加机构标签
        https://docs.eeo.cn/api/zh-hans/school/addSchoolLabel.html

        :param label_name: 标签名称
        """
        return self._post(
            params={'action': 'addSchoolLabel'},
            data=optionaldict({
                'labelName': label_name,
            }),
            result_processor=lambda x: x['labelId']
        )

    def update_school_label(
            self,
            label_id,
            label_name,
    ):
        """
        修改机构标签
        https://docs.eeo.cn/api/zh-hans/school/updateSchoolLabel.html

        :param label_id: 标签 ID
        :param type: 标签名称
        """
        return self._post(
            params={'action': 'updateSchoolLabel'},
            data=optionaldict({
                'labelId': label_id,
                'labelName': label_name,
            }),
        )

    def delete_school_label(
            self,
            label_id,
    ):
        """
        删除机构标签
        https://docs.eeo.cn/api/zh-hans/school/deleteSchoolLabel.html

        :param label_id: 标签 ID
        """
        return self._post(
            params={'action': 'deleteSchoolLabel'},
            data=optionaldict({
                'labelId': label_id,
            }),
        )
