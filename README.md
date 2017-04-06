＃ps： lijiejie脚本优化了下

import ds_store

if ds_store modules not exists:
	pip install https://pypi.python.org/packages/source/d/ds_store/ds_store-1.0.0.tar.gz

A .DS_Store file disclosure exploit. 

It parse .DS_Store file and download files recursively.

这是一个.DS\_Store文件泄漏利用脚本，它解析.DS_Store文件并递归地下载文件到本地。

    Usage: python mac_ds_store_.py http://www.example.com/.DS_Store
