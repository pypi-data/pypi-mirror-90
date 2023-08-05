# encoding: utf-8
from __future__ import absolute_import, unicode_literals

import json
from optionaldict import optionaldict

from .base import BaseAPI


class Broadcast(BaseAPI):
    """
    直播相关接口
    https://docs.eeo.cn/api/zh-hans/broadcast/
    """

    def set_class_video_multiple(
            self,
            course_id,
            class_info=()
    ):
        """
        课节设置录课、直播、回放（多个）
        https://docs.eeo.cn/api/zh-hans/broadcast/setClassVideoMultiple.html

        :param course_id: 课程 ID
        :param class_info: 课节信息数组
        """
        assert isinstance(class_info, (list, tuple))
        return self._post(
            params={'action': 'setClassVideoMultiple'},
            data=optionaldict({
                'courseId': course_id,
                'classJson': json.dumps(class_info),
            }),
        )

    def delete_class_video(
            self,
            class_id,
            file_id=None
    ):
        """
        删除单个课节视频
        https://docs.eeo.cn/api/zh-hans/broadcast/deleteClassVideo.html

        :param class_id: 课节 ID
        :param file_id: 课节下某个视频片段文件的ID
        """
        return self._post(
            params={'action': 'deleteClassVideo'},
            data=optionaldict({
                'classId': class_id,
                'fileId': file_id,
            }),
        )

    def update_class_lock_status(
            self,
            class_id,
            is_lock
    ):
        """
        修改课节锁定状态
        https://docs.eeo.cn/api/zh-hans/broadcast/updateClassLockStatus.html

        :param course_id: 课程 ID
        :param is_lock: 是否锁定
        """
        return self._post(
            params={'action': 'updateClassLockStatus'},
            data=optionaldict({
                'classId': class_id,
                'isLock': 1 if is_lock else 0,
            }),
        )

    def get_webcast_url(
            self,
            course_id,
            class_id=None
    ):
        """
        获取课程直播/回放播放器地址
        https://docs.eeo.cn/api/zh-hans/broadcast/getWebcastUrl.html

        :param course_id: 课程 ID
        :param class_id: 课节 ID
        """
        return self._post(
            params={'action': 'getWebcastUrl'},
            data=optionaldict({
                'courseId': course_id,
                'classId': class_id,
            }),
        )

    def get_webcast_partner_url(
            self,
            account,
            nick_name,
            course_id,
            class_id=None,
            partner_url='https://www.eeo.cn/webcast_partner.html'
    ):
        """
        获取课程直播/回放播放器免二次登陆地址
        https://docs.eeo.cn/api/zh-hans/broadcast/getWebcastUrl.html

        :param account: 账户
        :param nick_name: 昵称
        :param course_id: 课程 ID
        :param class_id: 课节 ID
        :param partner_url: url前缀
        """
        url = self.get_webcast_url(course_id, class_id)
        return self.get_webcast_partner_url_by_url(account, nick_name, url, partner_url)

    def get_webcast_partner_url_by_url(
            self,
            account,
            nick_name,
            url,
            partner_url='https://www.eeo.cn/webcast_partner.html'
    ):
        """
        获取课程直播/回放播放器免二次登陆地址
        https://docs.eeo.cn/api/zh-hans/broadcast/getWebcastUrl.html

        :param account: 账户
        :param nick_name: 昵称
        :param url: 接口获取到的url
        :param partner_url: url前缀
        """
        return self._client.get_partner_url(account, nick_name, url, 'courseKey', partner_url)

    def get_login_linked(
            self,
            uid,
            class_id,
            course_id,
            life_time=86400,
            device_type=1
    ):
        """
        获取唤醒客户端并进入教室链接
        https://docs.eeo.cn/api/zh-hans/getLoginLinked.html

        :param uid: 用户 UID
        :param class_id: 课节 ID
        :param course_id: 课程 ID
        :param life_time: 密钥有效时长（单位：秒）
        :param device_type: 1代表 Windows/Mac OS 端；2代表 iOS 移动端；3代表 Android
        """
        return self._post(
            params={'action': 'getLoginLinked'},
            data=optionaldict({
                'uid': uid,
                'lifeTime': life_time,
                'courseId': course_id,
                'classId': class_id,
                'deviceType': device_type,
            }),
        )
