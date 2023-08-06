## 多平台剪贴板复制工具

* 服务端发布版本前，需要手动修改docker-compose.yml中的版本，使版本与tag的版本一致
* 客户端
    1. linux版本使用pip安装，由于wxpython编译问题，可能需要手动安装wxpython后，再安装该软件
        - pip安装wxpython参考https://wxpython.org/pages/downloads/index.html
        - conda安装wxpython，需要先安装conda软件，然后执行conda install wxpython
        - linux源码安装： python setup.py install
    2. windows版本直接执行exe文件即可
    3. mac版本待发布