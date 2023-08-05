# encoding: utf-8
from __future__ import absolute_import, unicode_literals

from optionaldict import optionaldict

from .base import BaseAPI


class Cloud(BaseAPI):
    """
    云盘相关接口
    https://docs.eeo.cn/api/zh-hans/cloud/
    """
    API_BASE_URL = '/partner/api/cloud.api.php'

    def get_folder_list(
            self,
    ):
        """
        获取云盘文件夹列表
        https://docs.eeo.cn/api/zh-hans/cloud/getFolderList.html
        """
        return self._post(
            params={'action': 'getFolderList'},
        )

    def get_cloud_list(
            self,
            folder_id=None
    ):
        """
        获取指定文件夹下的文件夹及文件夹列表
        https://docs.eeo.cn/api/zh-hans/cloud/getCloudList.html

        :param folder_id: 文件夹 ID
        """
        return self._post(
            params={'action': 'getCloudList'},
            data=optionaldict({
                'folderId': folder_id
            }),
            result_processor=lambda x: x['folder_list']
        )

    def get_top_folder_id(
            self
    ):
        """
        获取顶级文件夹 ID
        https://root_url/partner/api/cloud.api.php?action=getTopFolderId
        """
        return self._post(
            params={'action': 'getTopFolderId'}
        )

    def upload_file(
            self,
            folder_id,
            file
    ):
        """
        上传文件
        https://docs.eeo.cn/api/zh-hans/cloud/uploadFile.html

        :param folder_id: 文件夹 ID
        :param file: 上传的文件, 一个 File-object
        """
        return self._post(
            params={'action': 'uploadFile'},
            data=optionaldict({
                'folderId': folder_id
            }),
            files={'Filedata': file}
        )

    def rename_file(
            self,
            file_id,
            file_name
    ):
        """
        重命名文件
        https://docs.eeo.cn/api/zh-hans/cloud/renameFile.html

        :param file_id: 文件 ID
        :param file_name: 文件名称
        """
        return self._post(
            params={'action': 'renameFile'},
            data=optionaldict({
                'fileId': file_id,
                'fileName': file_name
            })
        )

    def del_file(
            self,
            file_id
    ):
        """
        删除文件
        https://docs.eeo.cn/api/zh-hans/cloud/delFile.html

        :param file_id: 文件 ID
        """
        return self._post(
            params={'action': 'delFile'},
            data=optionaldict({
                'fileId': file_id
            })
        )

    def create_folder(
            self,
            folder_id,
            folder_name
    ):
        """
        创建文件夹
        https://docs.eeo.cn/api/zh-hans/cloud/createFolder.html

        :param folder_id: 文件夹 ID
        :param folder_name: 文件夹名称
        """
        return self._post(
            params={'action': 'createFolder'},
            data=optionaldict({
                'folderId': folder_id,
                'folderName': folder_name
            })
        )

    def rename_folder(
            self,
            folder_id,
            folder_name
    ):
        """
        重命名文件夹
        https://docs.eeo.cn/api/zh-hans/cloud/renameFolder.html

        :param folder_id: 文件夹 ID
        :param folder_name: 文件夹名称
        """
        return self._post(
            params={'action': 'renameFolder'},
            data=optionaldict({
                'folderId': folder_id,
                'folderName': folder_name
            })
        )

    def del_folder(
            self,
            folder_id
    ):
        """
        重命名文件夹
        https://docs.eeo.cn/api/zh-hans/cloud/delFolder.html

        :param folder_id: 文件夹 ID
        """
        return self._post(
            params={'action': 'delFolder'},
            data=optionaldict({
                'folderId': folder_id
            })
        )
