#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: uri.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""
import json
import requests
import socketio
import time
from pyperclip import paste, copy
from client.uri.loop import Loop
from client.uri.os_property import os_and_user_name
from client.client_log.logging import logging


def wait_for_new_paste(interval=0.5):
    originalText = paste()
    while True:
        currentText = paste()
        if currentText != originalText:
            return currentText
        time.sleep(interval)


def get_chipboard():
    ret = wait_for_new_paste()
    return ret


def log_detail(*args):
    # logging.error(f'callback recorded {args}')
    pass


USER_LIST = []


class AppRequest:
    def __init__(self, url):
        if not isinstance(url, str):
            url = str(url)

        self.base_url = url
        self.token = ''

    def register(self, user, pw, pw_ag):
        register_url = self.base_url + '/register'
        data = {'username': user, 'password': pw, 'password2': pw_ag}
        headers = {
            'content-type': 'application/json',
            }
        response = requests.post(register_url, data=json.dumps(data),
                                 headers=headers)
        return response.text

    def login(self, user, pw):
        login_url = self.base_url + '/login'
        data = {'username': user, 'password': pw}
        headers = {
            "content-type": "application/json",
            }
        try:
            response = requests.post(login_url, data=json.dumps(data),
                                     headers=headers)
            self.token = response.json()
        except Exception as e:
            logging.error(f'Failed to login to server, details is {e}')
            return {'code': 404,
                    'message': f'Failed to login to server, details is {e}'}

        return response.json()


class SocketClient:
    def __init__(self, url, pipe_data, connection):
        if not isinstance(url, str):
            url = str(url)
        self.url = url
        self._pipe_data = pipe_data
        self._connection = connection
        self.sio = socketio.Client()
        self._loop = None
        self.os_name = os_and_user_name()

    def connect(self, token):
        self.sio.connect(
            self.url, headers={'Authorization': token, 'client': self.os_name},
            namespaces=['/ucnp'])

    def start(self):
        self._loop = Loop(get_chipboard, interval=0)
        logging.debug('start waiting for ctrl + c')
        for ret in self._loop.start():
            data = {"ignore_sid": self._connection.ignored_sids(),
                    "content": ret}
            self.sio.emit('message', data, callback=log_detail,
                          namespace='/ucnp')

        self.sio.wait()

    def stop(self):
        logging.info('stop monitor and socket client')
        if self._loop:
            self._loop.stop()

        self.sio.disconnect()

    def register_namespace(self):
        self.sio.register_namespace(
            UriGet(self._pipe_data, self._connection, '/ucnp'))
        logging.info('Monitor namespace [ucnp] for user successfully started '
                     '========')
        self.sio.wait()


class UriGet(socketio.ClientNamespace):
    def __init__(self, pipe_data, connection, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pipe_data = pipe_data
        self._connection = connection

    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def on_message(self, data):
        self._pipe_data.add(data)
        copy(data)

    def on_online_users(self, data):
        self._connection.update(data)
