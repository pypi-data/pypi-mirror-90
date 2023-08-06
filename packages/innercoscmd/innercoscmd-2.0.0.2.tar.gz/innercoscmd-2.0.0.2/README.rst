INNERCOSCMD 
fork自腾讯云coscmd，修复相关API，用于支持innercos。底层依赖<http://git.code.oa.com/maysonshen/innercos-python-sdk-v5.git>

欢迎大家PR


COSCMD
#######################

.. image:: https://img.shields.io/pypi/v/coscmd.svg
   :target: https://pypi.org/search/?q=coscmd
   :alt: Pypi
.. image:: https://travis-ci.org/tencentyun/coscmd.svg?branch=master
   :target: https://travis-ci.org/tencentyun/coscmd
   :alt: Travis CI 

介绍
_______

腾讯云COS命令行工具, 目前可以支持Python2.6与Python2.7以及Python3.x。

安装指南
__________

使用pip安装 ::

    pip install -U innercoscmd

手动安装::

    python setup.py install

使用方法
__________

使用coscmd，参照 https://cloud.tencent.com/document/product/436/10976

由于innercos与腾讯云cos有一定的差异,服务端check只有sha1，没有md5. 使用的时候请`--verify sha1`
