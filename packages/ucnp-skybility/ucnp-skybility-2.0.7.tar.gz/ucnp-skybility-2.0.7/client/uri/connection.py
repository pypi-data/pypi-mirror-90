#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File:
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""

import time


class Connection:
    INSTANCE = None

    def __new__(cls, *args, **kwargs):
        if not cls.INSTANCE:
            cls.INSTANCE = super().__new__(cls)

        return cls.INSTANCE

    def __init__(self):
        # ['all_clients']
        self._current_clients = []

        # ['hostname', 'hostname2]
        self._ignore_clients = []

        #  {'hostname': ['sid1', 'sid2]}
        self._client_and_sid = {}

    def ignored_sids(self):
        ignored_sids = []
        for client in self.ignore_clients:
            ignored_sids.extend(self._client_and_sid.get(client, []))

        return ignored_sids

    def update(self, data):
        self._client_and_sid = {}
        self._current_clients = []
        for client in data:
            for hostname, sid in client.items():
                if hostname not in self._client_and_sid:
                    self._client_and_sid[hostname] = [sid]
                else:
                    self._client_and_sid[hostname].append(sid)

                if hostname not in self._current_clients:
                    self._current_clients.append(hostname)

    @property
    def current_clients(self):
        return self._current_clients

    @property
    def ignore_clients(self):
        return self._ignore_clients

    def add_ignore_client(self, ignore_client):
        if ignore_client not in self._current_clients:
            return

        if isinstance(ignore_client, list):
            self._ignore_clients.extend(ignore_client)

        elif isinstance(ignore_client, str):
            self._ignore_clients.append(ignore_client)

    def remove_ignore_client(self, ignore_client):
        if ignore_client not in self._current_clients:
            return

        if isinstance(ignore_client, list):
            for x in ignore_client:
                self._ignore_clients.remove(ignore_client)

        elif isinstance(ignore_client, str):
            self._ignore_clients.remove(ignore_client)


class PipeData:
    def __init__(self):
        self._data = ['', '', '', '', '']

    def add(self, data):
        if not len(data):
            return

        now = time.strftime('%Y-%m-%d %H:%M:%S : ')
        data = now + data
        self._data.insert(0, data)

    def __call__(self, *args, **kwargs):
        ret = []
        data = self._data[:5]
        for _d in data:
            if len(_d):
                ret.append(_d)
        return ret


connection = Connection()
