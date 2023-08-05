##########################
ClassIn Sdk for Python
##########################
.. image:: https://travis-ci.com/007gzs/classin.svg?branch=master
       :target: https://travis-ci.com/007gzs/classin
.. image:: https://img.shields.io/pypi/v/classin.svg
       :target: https://pypi.org/project/classin

ClassIn Python SDK。
`【阅读文档】 <http://classin.readthedocs.io/zh_CN/latest/>`_。

********
安装
********

目前 classin-sdk 支持的 Python 环境有 2.7, 3.4, 3.5, 3.6, 3.7 和 pypy。

为了简化安装过程，推荐使用 pip 进行安装

.. code-block:: bash

    pip install classin

升级 classin 到新版本::

    pip install -U classin

如果需要安装 GitHub 上的最新代码::

    pip install https://github.com/007gzs/classin/archive/master.zip


调用示例
********
 ::

    from classin import ClassInClient

    client = ClassInClient('<SID>', '<SECRET>')

    folders = client.cloud.get_folder_list()
