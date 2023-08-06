#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: loop.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""
import platform
import re
from subprocess import Popen, PIPE
import sys
import pinyin
import uuid
from client.client_log.logging import logging


def to_native_str(text):
    if sys.version_info[0] >= 3:
        if isinstance(text, bytes):
            try:
                text = text.decode('utf-8')
            except ValueError:
                try:
                    text = text.decode('gb2312')
                    text = pinyin.get(text, format='strip')
                except ValueError:
                    text = uuid.getnode()

    else:
        if isinstance(text, unicode):  # noqa: F821
            text = text.encode('utf-8')

    return text


def os_and_user_name():
    name = ''
    if platform.system() == 'Linux':
        hostname = _exec_cmd('hostname')
        user = _exec_cmd('whoami')
        name = re.sub(r'[\n\r\\ ]', '', f'{hostname}@{user}')
    elif platform.system() == 'Windows':
        name = re.sub(r'[\n\r\\ ]', '', _exec_cmd('whoami'))

    logging.info(f'get os_and_user name of this machine [{name}]')
    return name


def _exec_cmd(cmd):
    if isinstance(cmd, str):
        cmd = [cmd]

    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    ret, err = p.communicate()
    ret = to_native_str(ret)
    return ret
