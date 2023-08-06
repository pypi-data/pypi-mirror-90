#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: __init__.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""
import os

user_home = os.path.expanduser("~")
exe_path = os.path.dirname(os.path.abspath(__file__))
log_home = os.path.join(user_home, '.config', 'ucnp', 'log')
data_home = os.path.join(user_home, '.config', 'ucnp', 'data')
if not os.path.exists(data_home):
    os.makedirs(data_home, exist_ok=True)

if not os.path.exists(log_home):
    os.makedirs(log_home, exist_ok=True)
