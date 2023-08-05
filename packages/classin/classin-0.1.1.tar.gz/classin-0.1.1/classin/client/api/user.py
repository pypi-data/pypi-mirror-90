# encoding: utf-8
from __future__ import absolute_import, unicode_literals

import json

from optionaldict import optionaldict

from .base import BaseAPI


class User(BaseAPI):
    """
    用户相关接口
    https://docs.eeo.cn/api/zh-hans/user/
    """

    def register(
            self,
            telephone,
            nick_name=None,
            password=None,
            md5pass=None,
            file_data=None,
            add_to_school_member=0
    ):
        """
        注册用户
        https://docs.eeo.cn/api/zh-hans/user/register.html

        :param telephone: 注册手机号
        :param nick_name: 昵称、姓名
        :param password: 明文密码
        :param md5pass: MD5 加密密码
        :param file_data: 用户头像文件
        :param add_to_school_member: 0 不加为机构成员；1 加为机构学生；2 加为机构老师；
        """
        if add_to_school_member not in (1, 2, '1', '2'):
            add_to_school_member = 0
        assert (password is None) != (md5pass is None), "password 和 md5pass 二选一"

        return self._post(
            params={'action': 'register'},
            data=optionaldict({
                'telephone': telephone,
                'nickname': nick_name,
                'password': password,
                'md5pass': md5pass,
                'addToSchoolMember': add_to_school_member,
            }),
            files=optionaldict({
                'Filedata': file_data,
            }),
        )

    def register_multiple(
            self,
            users_info
    ):
        """
        注册用户（多个）
        https://docs.eeo.cn/api/zh-hans/user/registerMultiple.html

        :param users_info: 批量注册的用户数据
        """
        assert isinstance(users_info, (list, tuple))

        return self._post(
            params={'action': 'registerMultiple'},
            data=optionaldict({
                'userJson': json.dumps(users_info),
            }),
        )

    def modify_password(
            self,
            uid,
            old_md5_pass,
            password=None,
            md5pass=None
    ):
        """
        修改用户密码
        https://docs.eeo.cn/api/zh-hans/user/modifyPassword.html

        :param uid: 用户 UID
        :param old_md5_pass: 原 MD5 密码
        :param password: 新密码
        :param md5pass: 新 MD5 密码
        """
        assert (password is None) != (md5pass is None), "password 和 md5pass 二选一"

        return self._post(
            params={'action': 'modifyPassword'},
            data=optionaldict({
                'uid': uid,
                'oldMd5pass': old_md5_pass,
                'password': password,
                'md5pass': md5pass,
            }),
        )

    def add_school_student(
            self,
            student_account,
            student_name
    ):
        """
        添加学生
        https://docs.eeo.cn/api/zh-hans/user/addSchoolStudent.html

        :param student_account: 学生账号
        :param student_name: 学生名字
        """

        return self._post(
            params={'action': 'addSchoolStudent'},
            data=optionaldict({
                'studentAccount': student_account,
                'studentName': student_name,
            }),
        )

    def edit_school_student(
            self,
            student_uid,
            student_name
    ):
        """
        编辑学生信息
        https://docs.eeo.cn/api/zh-hans/user/editSchoolStudent.html

        :param student_uid: 注册成功后返回的用户 UID
        :param student_name: 学生的姓名
        """

        return self._post(
            params={'action': 'editSchoolStudent'},
            data=optionaldict({
                'studentUid': student_uid,
                'studentName': student_name,
            }),
        )

    def add_teacher(
            self,
            teacher_account,
            teacher_name,
            file_data=None
    ):
        """
        添加老师
        https://docs.eeo.cn/api/zh-hans/user/addTeacher.html

        :param teacher_account: 老师的账号
        :param teacher_account: 老师的姓名
        :param teacher_account:     老师的头像
        """

        return self._post(
            params={'action': 'addTeacher'},
            data=optionaldict({
                'teacherAccount': teacher_account,
                'teacherName': teacher_name,
            }),
            files=optionaldict({
                'Filedata': file_data,
            }),
        )

    def edit_teacher(
            self,
            teacher_name,
            st_id=None,
            teacher_uid=None,
            file_data=None
    ):
        """
        编辑老师
        https://docs.eeo.cn/api/zh-hans/user/editTeacher.html

        :param teacher_name: 老师的姓名
        :param st_id: 老师和机构对应的 ID
        :param teacher_uid: 手机账号的 UID
        :param file_data: 老师的头像
        """
        assert st_id is not None and teacher_uid is not None, "st_id, teacher_uid 至少传一个"

        return self._post(
            params={'action': 'editTeacher'},
            data=optionaldict({
                'st_id': st_id,
                'teacherUid': teacher_uid,
                'teacherName': teacher_name,
            }),
            files=optionaldict({
                'Filedata': file_data,
            }),
        )

    def stop_using_teacher(
            self,
            teacher_uid
    ):
        """
        停用老师
        https://docs.eeo.cn/api/zh-hans/user/stopUsingTeacher.html

        :param teacher_uid: 老师 UID
        """

        return self._post(
            params={'action': 'stopUsingTeacher'},
            data=optionaldict({
                'teacherUid': teacher_uid,
            }),
        )

    def restart_using_teacher(
            self,
            teacher_uid
    ):
        """
        启用老师
        https://docs.eeo.cn/api/zh-hans/user/restartUsingTeacher.html

        :param teacher_uid: 老师 UID
        """

        return self._post(
            params={'action': 'restartUsingTeacher'},
            data=optionaldict({
                'teacherUid': teacher_uid,
            }),
        )

    def update_class_student_comment(
            self,
            class_id,
            comments_info
    ):
        """
        更新课节教师对学生评价
        https://docs.eeo.cn/api/zh-hans/user/updateClassStudentComment.html

        :param class_id: 课节 ID
        :param comments_info: 评论数据结构
        """
        assert isinstance(comments_info, (list, tuple))

        return self._post(
            params={'action': 'updateClassStudentComment'},
            data=optionaldict({
                'classId': class_id,
                'commentJson': json.dumps(comments_info),
            }),
        )
