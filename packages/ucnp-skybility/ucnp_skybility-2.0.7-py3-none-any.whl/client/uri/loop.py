#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: loop.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""

from time import sleep


class Loop:
    def __init__(self, func, interval, *args):
        self.func = func
        self.interval = int(interval)
        self._exit = False
        self._execute_once = False
        self.args = args

    def start(self):
        if self._execute_once:
            ret = self.func(self.args)
            yield ret
            return

        while not self._exit:
            if self.args:
                ret = self.func(self.args)
            else:
                ret = self.func()

            yield ret

            if self.interval:
                sleep(self.interval)

    def stop(self):
        self._exit = True
