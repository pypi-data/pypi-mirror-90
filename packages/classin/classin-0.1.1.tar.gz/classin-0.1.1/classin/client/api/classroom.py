# encoding: utf-8
from __future__ import absolute_import, unicode_literals

import json
import datetime

from optionaldict import optionaldict

from .base import BaseAPI


class ClassRoom(BaseAPI):
    """
    教室内相关接口
    https://docs.eeo.cn/api/zh-hans/classroom/
    """

    def add_course(
            self,
            course_name,
            folder_id=None,
            file_data=None,
            expiry_time=None,
            main_teacher_uid=None,
            course_introduce=None,
            classroom_setting_id=None,
            course_unique_identity=None,
            allow_add_friend=True,
    ):
        """
        创建课程
        https://docs.eeo.cn/api/zh-hans/classroom/addCourse.html

        :param course_name: 课程名称
        :param folder_id: 可用资源文件夹 ID
        :param file_data: 上传的课程封面图片
        :param expiry_time: 过期时间
        :param main_teacher_uid: 班主任 UID
        :param course_introduce: 课程简介
        :param classroom_setting_id: 教室设置 ID
        :param course_unique_identity: 唯一标识
        :param allow_add_friend: 是否允许班级成员在群里互相添加好友
        """
        if isinstance(expiry_time, datetime.datetime):
            expiry_time = int(expiry_time.timestamp())
        return self._post(
            params={'action': 'addCourse'},
            data=optionaldict({
                'courseName': course_name,
                'folderId': folder_id,
                'expiryTime': expiry_time,
                'mainTeacherUid': main_teacher_uid,
                'courseIntroduce': course_introduce,
                'classroomSettingId': classroom_setting_id,
                'courseUniqueIdentity': course_unique_identity,
                'allowAddFriend': 1 if allow_add_friend else 0,
            }),
            files=optionaldict({
                'Filedata': file_data,
            })
        )

    def edit_course(
            self,
            course_id,
            folder_id=None,
            course_name=None,
            expiry_time=None,
            main_teacher_uid=None,
            stamp=True,
            file_data=None,
            course_introduce=None,
            classroom_setting_id=None,
            allow_add_friend=True,
    ):
        """
        编辑课程
        https://docs.eeo.cn/api/zh-hans/classroom/editCourse.html

        :param course_id: 课程 ID
        :param folder_id: 可用资源文件夹 ID
        :param course_name: 课程名称
        :param expiry_time: 过期时间
        :param main_teacher_uid: 班主任 UID
        :param stamp: 原班主任是否加入教师列表
        :param file_data: 上传的课程封面图片
        :param course_introduce: 课程简介
        :param classroom_setting_id: 教室设置 ID
        :param allow_add_friend: 是否允许班级成员在群里互相添加好友
        """
        if allow_add_friend is not None:
            allow_add_friend = 1 if allow_add_friend else 0
        return self._post(
            params={'action': 'editCourse'},
            data=optionaldict({
                'courseId': course_id,
                'courseName': course_name,
                'folderId': folder_id,
                'expiryTime': expiry_time,
                'mainTeacherUid': main_teacher_uid,
                'stamp': 1 if stamp else 0,
                'courseIntroduce': course_introduce,
                'classroomSettingId': classroom_setting_id,
                'allowAddFriend': allow_add_friend,
            }),
            files=optionaldict({
                'Filedata': file_data,
            })
        )

    def end_course(
            self,
            course_id,
    ):
        """
        结束课程
        https://docs.eeo.cn/api/zh-hans/classroom/endCourse.html

        :param course_id: 课程 ID
        """
        return self._post(
            params={'action': 'endCourse'},
            data=optionaldict({
                'courseId': course_id,
            }),
        )

    def get_live_partner_url(
            self,
            account,
            nick_name,
            live_url,
            partner_url='https://www.eeo.cn/live_partner.php',
    ):
        """
        课节直播播放器地址免二次登陆地址
        https://docs.eeo.cn/api/zh-hans/classroom/addCourseClass.html

        :param account: 账户
        :param nick_name: 昵称
        :param live_url: 接口获取到的url
        :param partner_url: url前缀
        """
        return self._client.get_partner_url(account, nick_name, live_url, 'lessonKey', partner_url)

    def add_course_class(
            self,
            course_id,
            class_name,
            begin_time,
            end_time,
            teacher_uid,
            folder_id=None,
            seat_num=6,
            record=False,
            live=False,
            replay=False,
            assistant_uid=None,
            is_auto_onstage=False,
            is_hd=0,
            course_unique_identity=None,
            class_introduce=None,
            watch_by_login=False,
            allow_unlogged_chat=True,
    ):
        """
        创建课节(单个)
        https://docs.eeo.cn/api/zh-hans/classroom/addCourseClass.html

        :param course_id: 课程 ID
        :param class_name: 课节名称
        :param begin_time: 上课时间
        :param end_time: 下课时间
        :param teacher_uid: 教师 UID
        :param folder_id: 云盘目录 ID
        :param seat_num: 学生上台数
        :param record: 是否开启录课
        :param live: 是否开启直播
        :param replay: 是否开启回放
        :param assistant_uid: 助教 UID
        :param is_auto_onstage: 学生进入教室时是否自动上台
        :param is_hd: 是否高清 0=非高清，1=高清，2=全高清
        :param course_unique_identity: 唯一标识
        :param class_introduce: 课节简介
        :param watch_by_login: 是否只有扽牢固
        :param allow_unlogged_chat: 是否允许未登录用户参与直播聊天和点赞
        """
        if isinstance(begin_time, datetime.datetime):
            begin_time = int(begin_time.timestamp())
        if isinstance(end_time, datetime.datetime):
            end_time = int(end_time.timestamp())
        return self._post(
            params={'action': 'addCourseClass'},
            data=optionaldict({
                'courseId': course_id,
                'className': class_name,
                'beginTime': begin_time,
                'endTime': end_time,
                'teacherUid': teacher_uid,
                'folderId': folder_id,
                'seatNum': seat_num,
                'record': 1 if record else 0,
                'live':  1 if live else 0,
                'replay':  1 if replay else 0,
                'assistantUid': assistant_uid,
                'isAutoOnstage':  1 if is_auto_onstage else 0,
                'isHd': is_hd,
                'courseUniqueIdentity': course_unique_identity,
                'classIntroduce': class_introduce,
                'watchByLogin':  1 if watch_by_login else 0,
                'allowUnloggedChat':  1 if allow_unlogged_chat else 0,
            }),
        )

    def add_course_class_multiple(
            self,
            course_id,
            classes_info
    ):
        """
        创建课节(多个)
        https://docs.eeo.cn/api/zh-hans/classroom/addCourseClassMultiple.html

        :param course_id: 课程 ID
        :param classes_info: 课节信息数组
        """
        assert isinstance(classes_info, (list, tuple))
        return self._post(
            params={'action': 'addCourseClassMultiple'},
            data=optionaldict({
                'courseId': course_id,
                'classJson': json.dumps(classes_info),
            }),
        )

    def edit_course_class(
            self,
            course_id,
            class_id,
            class_name=None,
            begin_time=None,
            end_time=None,
            teacher_uid=None,
            folder_id=None,
            record=None,
            live=None,
            replay=None,
            assistant_uid=None,
            is_auto_onstage=None,
            class_introduce=None,
            watch_by_login=None,
            allow_unlogged_chat=None,
    ):
        """
        修改课节信息
        https://docs.eeo.cn/api/zh-hans/classroom/editCourseClass.html

        :param course_id: 课程 ID
        :param class_id: 课节 ID
        :param class_name: 课节名称
        :param begin_time: 上课时间
        :param end_time: 下课时间
        :param teacher_uid: 教师 UID
        :param folder_id: 云盘目录 ID
        :param record: 是否开启录课
        :param live: 是否开启直播
        :param replay: 是否开启回放
        :param assistant_uid: 助教 UID
        :param is_auto_onstage: 学生进入教室时是否自动上台
        :param class_introduce: 课节简介
        :param watch_by_login: 是否只有扽牢固
        :param allow_unlogged_chat: 是否允许未登录用户参与直播聊天和点赞
        """
        def _to_bool(_value):
            if isinstance(_value, bool):
                return 1 if _value else 0
            else:
                return _value
        if isinstance(begin_time, datetime.datetime):
            begin_time = int(begin_time.timestamp())
        if isinstance(end_time, datetime.datetime):
            end_time = int(end_time.timestamp())

        return self._post(
            params={'action': 'editCourseClass'},
            data=optionaldict({
                'courseId': course_id,
                'classId': class_id,
                'className': class_name,
                'beginTime': begin_time,
                'endTime': end_time,
                'teacherUid': teacher_uid,
                'folderId': folder_id,
                'record': _to_bool(record),
                'live': _to_bool(live),
                'replay': _to_bool(replay),
                'assistantUid': assistant_uid,
                'isAutoOnstage': _to_bool(is_auto_onstage),
                'classIntroduce': class_introduce,
                'watchByLogin': _to_bool(watch_by_login),
                'allowUnloggedChat': _to_bool(allow_unlogged_chat),
            }),
        )

    def modify_class_seat_num(
            self,
            course_id,
            class_id,
            seat_num,
            is_hd=0
    ):
        """
        修改课节上台学生数
        https://docs.eeo.cn/api/zh-hans/classroom/modifyClassSeatNum.html

        :param course_id: 课程 ID
        :param class_id: 课节 ID
        :param seat_num: 上台学生数
        :param is_hd: 是否高清 0=非高清，1=高清，2=全高清
        """
        return self._post(
            params={'action': 'modifyClassSeatNum'},
            data=optionaldict({
                'courseId': course_id,
                'classId': class_id,
                'seatNum': seat_num,
                'isHd': is_hd,
            }),
        )

    def del_course_class(
            self,
            course_id,
            class_id,
    ):
        """
        删除课节
        https://docs.eeo.cn/api/zh-hans/classroom/delCourseClass.html

        :param course_id: 课程 ID
        :param class_id: 课节 ID
        """
        return self._post(
            params={'action': 'delCourseClass'},
            data=optionaldict({
                'courseId': course_id,
                'classId': class_id,
            }),
        )

    def add_course_student(
            self,
            course_id,
            identity,
            student_uid,
            student_name=None
    ):
        """
        课程下添加学生/旁听（单个）
        https://docs.eeo.cn/api/zh-hans/classroom/addCourseStudent.html

        :param course_id: 课程 ID
        :param identity: 学生身份(1 为学生,2 为旁听)
        :param student_uid: 学生 UID
        :param student_name: 机构后台旁听生的姓名
        """
        return self._post(
            params={'action': 'addCourseStudent'},
            data=optionaldict({
                'courseId': course_id,
                'identity': identity,
                'studentUid': student_uid,
                'studentName': student_name,
            }),
        )

    def del_course_student(
            self,
            course_id,
            student_uid,
            identity=1,
    ):
        """
        课程下删除学生/旁听（单个）
        https://docs.eeo.cn/api/zh-hans/classroom/delCourseStudent.html

        :param course_id: 课程 ID
        :param identity: 学生身份(1 为学生,2 为旁听)
        :param student_uid: 学生 UID
        """
        return self._post(
            params={'action': 'delCourseStudent'},
            data=optionaldict({
                'courseId': course_id,
                'identity': identity,
                'studentUid': student_uid,
            }),
        )

    def add_course_student_multiple(
            self,
            course_id,
            students_info,
            identity=1,
    ):
        """
        课程下添加学生/旁听（多个）
        https://docs.eeo.cn/api/zh-hans/classroom/addCourseStudentMultiple.html

        :param course_id: 课程 ID
        :param identity: 学生身份(1 为学生,2 为旁听)
        :param students_info: 需要添加的帐号数组
        """
        assert isinstance(students_info, (list, tuple))
        return self._post(
            params={'action': 'addCourseStudentMultiple'},
            data=optionaldict({
                'courseId': course_id,
                'identity': identity,
                'studentJson': json.dumps(students_info),
            }),
        )

    def del_course_student_multiple(
            self,
            course_id,
            student_uids,
            identity=1,
    ):
        """
        课程下删除学生/旁听（多个）
        https://docs.eeo.cn/api/zh-hans/classroom/delCourseStudentMultiple.html

        :param course_id: 课程 ID
        :param identity: 学生身份(1 为学生,2 为旁听)
        :param student_uids: 需要删除学生UID数组
        """
        assert isinstance(student_uids, (list, tuple))
        return self._post(
            params={'action': 'delCourseStudentMultiple'},
            data=optionaldict({
                'courseId': course_id,
                'identity': identity,
                'studentUidJson': json.dumps(student_uids),
            }),
        )

    def add_class_student_multiple(
            self,
            course_id,
            class_id,
            students_info,
            identity=1,
    ):
        """
        课节下添加学生（多个）
        https://docs.eeo.cn/api/zh-hans/classroom/addClassStudentMultiple.html

        :param course_id: 课程 ID
        :param class_id: 课节 ID
        :param students_info: 需要添加帐号数组
        :param identity: 学生身份(1 为学生,2 为旁听)
        """
        assert isinstance(students_info, (list, tuple))
        return self._post(
            params={'action': 'addClassStudentMultiple'},
            data=optionaldict({
                'courseId': course_id,
                'classId': class_id,
                'identity': identity,
                'studentJson': json.dumps(students_info),
            }),
        )

    def del_class_student_multiple(
            self,
            course_id,
            class_id,
            student_uids,
            identity=1,
    ):
        """
        课节下删除学生（多个）
        https://docs.eeo.cn/api/zh-hans/classroom/delClassStudentMultiple.html

        :param course_id: 课程 ID
        :param class_id: 课节 ID
        :param student_uids: 需要删除学生UID数组
        :param identity: 学生身份(1 为学生,2 为旁听)
        """
        assert isinstance(student_uids, (list, tuple))
        return self._post(
            params={'action': 'delClassStudentMultiple'},
            data=optionaldict({
                'courseId': course_id,
                'classId': class_id,
                'identity': identity,
                'studentUidJson': json.dumps(student_uids),
            }),
        )

    def modify_course_teacher(
            self,
            course_id,
            teacher_uid
    ):
        """
        更换课程老师
        https://docs.eeo.cn/api/zh-hans/classroom/modifyCourseTeacher.html

        :param course_id: 课程 ID
        :param teacher_uid: 老师 UID
        """
        return self._post(
            params={'action': 'modifyCourseTeacher'},
            data=optionaldict({
                'courseId': course_id,
                'teacherUid': teacher_uid,
            }),
        )

    def remove_course_teacher(
            self,
            course_id,
            teacher_uid
    ):
        """
        移除课程老师
        https://docs.eeo.cn/api/zh-hans/classroom/removeCourseTeacher.html

        :param course_id: 课程 ID
        :param teacher_uid: 老师 UID
        """
        return self._post(
            params={'action': 'removeCourseTeacher'},
            data=optionaldict({
                'courseId': course_id,
                'teacherUid': teacher_uid,
            }),
        )

    def add_course_class_student(
            self,
            course_id,
            student_uid,
            class_ids
    ):
        """
        课程下多个课节添加学生
        https://docs.eeo.cn/api/zh-hans/classroom/addCourseClassStudent.html

        :param course_id: 课程 ID
        :param student_uid: 学生 UID
        :param class_ids: 课节 ID 数组
        """
        assert isinstance(class_ids, (list, tuple))
        return self._post(
            params={'action': 'addCourseClassStudent'},
            data=optionaldict({
                'courseId': course_id,
                'studentUid': student_uid,
                'classJson': json.dumps(class_ids),
            }),
        )

    def add_class_labels(
            self,
            course_id,
            classes_info
    ):
        """
        添加/修改/删除课节标签
        https://docs.eeo.cn/api/zh-hans/classroom/addClassLabels.html

        :param course_id: 课程 ID
        :param classes_info: 课节数组
        """
        assert isinstance(classes_info, (list, tuple))
        return self._post(
            params={'action': 'addClassLabels'},
            data=optionaldict({
                'courseId': course_id,
                'classList': json.dumps(classes_info),
            }),
        )
