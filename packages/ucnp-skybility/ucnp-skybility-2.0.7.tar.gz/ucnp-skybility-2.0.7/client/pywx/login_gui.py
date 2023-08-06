#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File:
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""
import os
import threading
import base64
import json
import wx
import wx.adv
import re
import platform
from pubsub import pub
from client.pywx.WxContext import TaskBar, LogUI, RegistUI, NormalUi, UI
from client.uri.uri import AppRequest, SocketClient
from client.client_log.logging import logging
from client import exe_path, data_home, log_home

logging.init_log(log_level=logging.WARNING, logger_name='engineio.client',
                 log_dir=log_home)
logging.init_log(log_level=logging.WARN, logger_name='socketio.client',
                 log_dir=log_home)
logging.init_log(log_level=logging.INFO,
                 log_dir=log_home)


class AppSend:
    def __init__(self, url):
        self._url: str = url
        self._valid_url()
        self._app = AppRequest(self._url)

    @property
    def app(self):
        return self._app

    def _valid_url(self):
        if not (self._url.startswith('http') | self._url.startswith('https')):
            self._url = 'http://' + self._url


class SockSend:
    def __init__(self, url, pipe_data, connection):
        self._url = url
        self._valid_url()
        self._sock = SocketClient(self._url, pipe_data, connection)

    @property
    def sock(self):
        return self._sock

    def _valid_url(self):
        if not (self._url.startswith('http') | self._url.startswith('https')):
            self._url = 'http://' + self._url


class App(wx.App):
    def OnExit(self):
        # LoginUI.graceful_exit()
        return 0


class MessageGui(UI):
    def __init__(self, pid, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_ok_dialog(f'ucnp is already running with pid [{pid}],'
                              f' no need to start again')


class LoginGui(LogUI):
    def __init__(self, pipe_data, connection, *args, **kwargs):
        self._server_url = ''
        self._username = ''
        self._pw = ''
        # self.window = None

        self._exe_path = exe_path
        self.pipe_data = pipe_data()
        self.connection = connection()
        self.service_started = False

        self._sender_thread = None
        self._receiver_thread = None
        self._socker = None

        self._connect_string_file = os.path.join(data_home,
                                                 'connect_string.txt')
        self._enable_save_pw_file = os.path.join(data_home,
                                                 'enable_save_password.txt')

        # kwargs["style"] = kwargs.get("style", 0)
        super().__init__(self._exe_path, *args, **kwargs)

        pub.subscribe(self.response_to_request_url, 'request_server_url')

        self.bind_btn()
        self.init_value()
        self.disable_sign_button()

        # problem unknown in windows
        if platform.system() == 'Windows':
            self.Iconize(True)
            self.Iconize(False)

    @property
    def exe_path(self):
        return self._exe_path

    def init_value(self):
        if not self.is_save_pw_enabled():
            return False

        if not os.path.exists(self._connect_string_file):
            return False

        ret = ['', '', '']
        with open(self._connect_string_file, 'r') as f:
            try:
                ret = json.load(f)
            except (TypeError, json.JSONDecodeError):
                pass

        server_url = base64.b64decode(ret[0].encode('utf-8'))
        user = base64.b64decode(ret[1].encode('utf-8'))
        word = base64.b64decode(ret[2].encode('utf-8'))

        self.server_text.SetValue(server_url)
        self.user_text.SetValue(user)
        self.password_text.SetValue(word)
        self.save_password.SetValue(True)
        return True

    def response_to_request_url(self, message):
        pub.sendMessage('server_url', message=self._server_url)

    def bind_btn(self):
        # current forget password is not available
        self.btn_forget_password.Disable()

        self.server_text.Bind(wx.EVT_TEXT, self.server_url)
        self.user_text.Bind(wx.EVT_TEXT, self.set_username)
        self.password_text.Bind(wx.EVT_TEXT, self.set_password)

        self.btn_sign_in.Bind(wx.EVT_BUTTON, self.login)
        self.btn_sign_up.Bind(wx.EVT_BUTTON, self.register)
        self.btn_sign_out.Bind(wx.EVT_BUTTON, self.logout)

        self.btn_forget_password.Bind(wx.EVT_BUTTON, self.find_password)
        self.save_password.Bind(wx.EVT_CHECKBOX, self.save_pw)

        self.Show(True)
        self.Center()

    def cook_tray(self, window):
        if not TaskBar.is_system_tray_available():
            return

        frame = wx.Frame(self)
        TaskBarIcon(self, frame)

    def server_url(self, event):
        obj = event.GetEventObject()
        self._server_url = obj.GetValue()

    def validate(self):
        # valid host ip
        if not self._server_url:
            self.create_ok_dialog('host or port should not be empty')
            logging.error('host or port should not be empty')
            return False

        # valid port
        return True

    def set_username(self, event):
        obj = event.GetEventObject()
        self._username = obj.GetValue()

    def set_password(self, event):
        obj = event.GetEventObject()
        self._pw = obj.GetValue()

    def try_login_without_message(self):
        token = AppSend(self._server_url).app.login(self._username,
                                                    self._pw)
        if token.get('code') == 0:
            arg = 'Bearer ' + token.get('data', {}).get('access_token', '')

            self._socker = SockSend(
                self._server_url, self.pipe_data, self.connection).sock
            self._socker.connect(arg)

            self._sender_thread = threading.Thread(
                target=self._socker.start, daemon=True)
            self._sender_thread.start()

            self._receiver_thread = threading.Thread(
                target=self._socker.register_namespace, daemon=True)
            self._receiver_thread.start()

            message = f'Succeed login into server [{self._server_url}]'
            logging.info(message)
            self._save_pw_to_file()
            self.service_started = True

            self._hide_gui()

        return token

    def login(self, event):
        logging.info(f'Login to server [{self._server_url}]')
        if not self.validate():
            self.disable_sign_button()
            return

        if self.service_started:
            self.disable_sign_button()
            self._hide_gui()
            logging.info(
                'Service has already started, ignore start action this time')
            return

        token = self.try_login_without_message()
        if token.get('code') == 0:
            self.disable_sign_button()
            return

        else:
            message = token.get('message', '')
            logging.info(
                f'Failed login into server [{self._server_url}]')
            self.create_ok_dialog(message + ",check your input.")
            # self.Close(True)

    def register(self, event):
        if not self._server_url:
            self.create_ok_dialog('Server URL not set')
            return

        RegisterUI(self.exe_path, self, wx.ID_ANY, "", size=(559, 450))

    def system_tray(self, event):
        self.Hide()

    def _hide_gui(self):
        if TaskBar.is_system_tray_available():
            self.Show(False)
        else:
            self.Iconize(True)

    def find_password(self, event):
        pass

    def save_pw(self, event):
        obj = event.GetEventObject()
        choose = obj.GetValue()
        if choose:
            self.enable_save_pw(True)
        else:
            self.enable_save_pw(False)

    def _save_pw_to_file(self):
        if self.save_password.GetValue():
            file = self._connect_string_file
            url = self._server_url.encode('utf-8')
            user = self._username.encode('utf-8')
            word = self._pw.encode('utf-8')
            data = (base64.b64encode(url).decode('utf-8'),
                    base64.b64encode(user).decode('utf-8'),
                    base64.b64encode(word).decode('utf-8')
                    )
            with open(file, 'w') as f:
                json.dump(data, f)

    def enable_save_pw(self, ret):
        file = self._enable_save_pw_file
        if not ret:
            with open(self._connect_string_file, 'w') as f:
                f.truncate()

        ret = str(ret)
        with open(file, 'w') as f:
            f.write(ret)

    def is_save_pw_enabled(self):
        file = self._enable_save_pw_file
        if not os.path.exists(file):
            return False

        with open(file, 'r') as f:
            if f.read() != 'True':
                return False

        return True

    def logout(self, event):
        if self._socker:
            self._socker.stop()

        self.service_started = False
        self.disable_sign_button()

    def stop(self):
        if self._socker:
            self._socker.stop()

        self.service_started = False

    def OnBtnExitClick(self, event):
        if not TaskBar.is_system_tray_available():
            self.stop()
            wx.Exit()

        self.Hide()
        return False

    def disable_sign_button(self):
        sign_in_label = {True: "Signed In", False: "Sign In"}
        sign_out_label = {True: "Sign Out", False: "Signed Out"}
        self.btn_sign_in.Enable(not self.service_started)
        self.btn_sign_out.Enable(self.service_started)

        self.btn_sign_out.SetLabel(sign_out_label.get(self.service_started))
        self.btn_sign_in.SetLabel(sign_in_label.get(self.service_started))


class RegisterUI(RegistUI):
    def __init__(self, exe_path, *args, **kwargs):
        # kwargs['style'] = 0
        super().__init__(exe_path, *args, **kwargs)

        self.user_name = ''
        self.pass_word = ''
        self.confirm_password = ''
        self.server_url = ''

        pub.subscribe(self.end_refresh_url, 'server_url')

        self.request_refresh_url()
        self.bind_btn()

        # problem unknown in windows
        if platform.system() == 'Windows':
            self.Iconize(True)
            self.Iconize(False)

    def request_refresh_url(self):
        pub.sendMessage('request_server_url', message='register ui')

    def end_refresh_url(self, message):
        self.server_url = message
        if not self.server_url:
            self.create_ok_dialog(
                'Server URL not set, go back to the login ui and set it!')

    def bind_btn(self):
        self.btn_ok.Bind(wx.EVT_BUTTON, self.confirm)
        self.username_text.Bind(wx.EVT_TEXT, self.username)
        self.pw_text.Bind(wx.EVT_TEXT, self.set_password)
        self.repw_text.Bind(wx.EVT_TEXT, self.confirm_passwords)

    def username(self, event):
        obj = event.GetEventObject()
        self.user_name = obj.GetValue()

    def set_password(self, event):
        obj = event.GetEventObject()
        self.pass_word = obj.GetValue()

    def confirm_passwords(self, event):
        obj = event.GetEventObject()
        self.confirm_password = obj.GetValue()

    def _valid_pw(self):
        _c = re.compile(r'^(?:(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])).{8,40}$')
        ret = _c.match(self.pass_word)
        return ret

    def confirm(self, event):
        if not self._valid_pw():
            message = 'Password not satisfy rules, \n' \
                      'must include [A-Za-z0-9] and length to 8 char,\n' \
                      'input again !!'
            self.create_question_dialog(message)
            return

        if self.confirm_password and self.pass_word:
            if self.confirm_password == self.pass_word:
                AppSend(self.server_url).app.register(
                    self.user_name,
                    self.pass_word,
                    self.confirm_password)
                self.Close()
                return

        message = 'password and confirm password mismatch,\nyou need input ' \
                  'again'
        self.create_question_dialog(message)


class TaskBarIcon(wx.adv.TaskBarIcon):
    # TRAY_HOST_INFO = ''

    def __init__(self, app: LoginGui, frame):
        self._frame = frame
        super().__init__()
        self._app = app
        self._tray_icon = os.path.join(
            self._app.exe_path, 'img', 'task_bar.png')
        # TaskBarIcon.TRAY_HOST_INFO = '{0}'.format('99')
        self.set_icon(self._tray_icon)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.show_balloon)

        self.task_bar = TaskBar(self)

    def set_icon(self, path):
        icon = wx.Icon(wx.Bitmap(path))
        self.SetIcon(icon, 'Skybility Ucnp')
        self.ShowBalloon('Ucnp', 'Skybility', msec=2)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        # self.task_bar.create_menu_item(menu, 'Show Gui', self.show_gui)

        # start service is equal to sign in in function
        self.task_bar.create_menu_item(menu, 'Start Service', self._app.login)

        # stop service is equal to sign out in function
        self.task_bar.create_menu_item(menu, 'Stop Service', self._app.logout)
        self.task_bar.chk_item_click(menu, 'Client List',
                                     self.block_special_user,
                                     self._app.connection)
        self.task_bar.chk_item_click(menu, 'Recent Content',
                                     self.show_recent_content,
                                     self._app.pipe_data())
        self.task_bar.create_menu_item(menu, 'Sign Out',
                                       self.sign_out_and_show_gui)
        self.task_bar.create_menu_item(menu, 'Log', self.show_log)
        self.task_bar.create_menu_item(menu, 'Exit', self.on_exit)

        return menu

    def sign_out_and_show_gui(self, event):
        self.show_gui(event)
        self._app.logout(event)

    @property
    def app(self):
        return self._app

    def click_if_not_clicked(self, event):
        pass

    def show_recent_content(self, index):
        def recent_content(event):
            content = self._app.pipe_data()[index]
            ui = NormalUi(self._frame, -1, "LOG", size=(659, 500))
            text = wx.TextCtrl(ui, -1, style=wx.TE_MULTILINE)
            text.write(content)
            ui.Show()

        return recent_content

    def show_log(self, event):
        content = ''
        file_path = os.path.join(log_home, 'up_utils.log')
        if os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                content = f.read()

        ui = NormalUi(self._frame, -1, "LOG", size=(659, 500))
        text = wx.TextCtrl(ui, -1, style=wx.TE_MULTILINE)
        logging.error(
            'show log for pipe data id is {0}'.format(id(self._app.pipe_data)))
        text.write(content)
        ui.Show()

    def block_special_user(self, index):
        def block_user_list(event):
            if index in self._app.connection.ignore_clients:
                self._app.connection.remove_ignore_client(index)
            elif index not in self._app.connection.ignore_clients:
                self._app.connection.add_ignore_client(index)

        return block_user_list

    def on_exit(self, event):
        self.Destroy()
        self.RemoveIcon()
        self._app.stop()
        self._app.Destroy()
        self._frame.Close(True)
        self._app.Close(True)
        logging.info('Stop ucnp Skybility now')
        wx.Exit()

    def show_balloon(self, event):
        # self.CreatePopupMenu()
        self.ShowBalloon('Ucnp', 'Skybility', msec=2)

    def show_gui(self, event):
        self._app.Show(True)
        self._app.Iconize(iconize=False)
