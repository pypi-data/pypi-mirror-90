#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: logging.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""
import os
import logging


def __init_log(log_level=logging.INFO, logger_name=None,
               log_dir=os.path.join("log", "client")):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    formatter = logging.Formatter(
        '%(asctime)s [%(name)s]: <%(levelname)s> %(message)s '
        '[%(filename)s:%(lineno)d:%(funcName)s]')

    log_dir = log_dir
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    log_file = logger_name
    if not log_file:
        log_file = 'up_utils'

    log_file = os.path.join(log_dir, log_file)

    if not log_file.endswith('.log'):
        log_file += '.log'

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    handler.setLevel(log_level)
    handler.name = 'test'

    logger.addHandler(handler)


def __set_proc_name(proc_name):
    logging.getLogger(proc_name)


setattr(logging, 'init_log', __init_log)
setattr(logging, 'set_proc_name', __set_proc_name)
