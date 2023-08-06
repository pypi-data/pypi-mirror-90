#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: WxContext.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2020, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""
import os
import wx
import wx.adv
import platform


class NormalUi(wx.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class UI(wx.Frame):
    def __init__(self, *args, **kwargs):
        kwargs['style'] = wx.MINIMIZE_BOX
        super().__init__(*args, **kwargs)

    def create_menu_bar(self, bind_func):
        menu_bar = wx.MenuBar()
        register_menu = wx.Menu()
        register_item = register_menu.Append(wx.ID_NEW, 'Register',
                                             helpString='register to add new '
                                                        'user')
        menu_bar.Append(register_menu, '&Register')
        self.SetMenuBar(menu_bar)

        self.Bind(wx.EVT_MENU, bind_func, register_item)
        return menu_bar

    def create_question_dialog(self, message='Demo message', exist=True):
        dlg = wx.MessageDialog(
            None, message=message,
            caption='Message',
            style=wx.YES_NO | wx.ICON_QUESTION)
        result = dlg.ShowModal()
        if result == wx.ID_NO and exist:
            if TaskBar.is_system_tray_available():
                self.Show(False)
            else:
                self.Close()

    def create_ok_dialog(self, message='Demo message'):
        dlg = wx.MessageDialog(None, message=message,
                               caption='Message',
                               style=wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()


class LogUI(UI):
    def __init__(self, exe_path, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._exe_path = exe_path
        self.panelTitleBar = wx.Panel(self, wx.ID_ANY)
        self.btnMinimize = wx.Button(self.panelTitleBar, wx.ID_ANY, "",
                                     style=wx.BORDER_NONE | wx.BU_NOTEXT)
        self.btnMaximize = wx.Button(self.panelTitleBar, wx.ID_ANY, "",
                                     style=wx.BORDER_NONE | wx.BU_NOTEXT)

        self.btnExit = wx.Button(self.panelTitleBar, wx.ID_ANY, "",
                                 style=wx.BORDER_NONE | wx.BU_NOTEXT)
        self.panelBody = wx.Panel(self, wx.ID_ANY)

        self.Bind(wx.EVT_BUTTON, self.OnBtnExitClick, self.btnExit)
        self.Bind(wx.EVT_BUTTON, self.OnBtnMinimizeClick, self.btnMinimize)
        self.Bind(wx.EVT_BUTTON, self.OnBtnMaximizeClick, self.btnMaximize)
        self.panelTitleBar.Bind(wx.EVT_LEFT_DOWN, self.OnTitleBarLeftDown)
        self.panelTitleBar.Bind(wx.EVT_MOTION, self.OnMouseMove)

        self.server = wx.StaticText(self.panelBody, wx.ID_ANY,
                                    label="Server URL:")
        self.user = wx.StaticText(self.panelBody, wx.ID_ANY,
                                  label="User Name:")
        self.password = wx.StaticText(self.panelBody, wx.ID_ANY,
                                      label="Password:")

        self.btn_sign_in = wx.Button(self.panelBody, wx.ID_ANY, "Sign In",
                                     size=(80, 38))
        self.btn_sign_up = wx.Button(self.panelBody, wx.ID_ANY, "Sign Up",
                                     size=(80, 38))
        self.btn_sign_out = wx.Button(self.panelBody, wx.ID_ANY, "Sign Out",
                                      size=(80, 38))

        self.server_text = wx.TextCtrl(self.panelBody, wx.ID_ANY,
                                       size=wx.Size(230, 40))
        self.server_text.SetBackgroundColour(wx.Colour(230, 230, 250))
        _font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.server.SetFont(_font)

        self.user_text = wx.TextCtrl(self.panelBody, wx.ID_ANY,
                                     size=wx.Size(230, 40))
        self.user_text.SetBackgroundColour(wx.Colour(230, 230, 250))
        _font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.user.SetFont(_font)

        self.password_text = wx.TextCtrl(self.panelBody, wx.ID_ANY,
                                         size=wx.Size(230, 40),
                                         style=wx.TE_PASSWORD)
        self.password_text.SetBackgroundColour(wx.Colour(230, 230, 250))
        _font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.password.SetFont(_font)

        self.save_password = wx.CheckBox(
            self.panelBody, wx.ID_ANY, label="Save Password")
        self.btn_forget_password = wx.Button(
            self.panelBody, style=wx.BORDER_NONE, label="forget password?")
        self.btn_forget_password.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.skybility_logo = wx.StaticBitmap(
            self.panelBody, wx.ID_ANY,
            wx.Bitmap(
                os.path.join(self._exe_path, "img", "skybility_logo.png"),
                wx.BITMAP_TYPE_ANY))

        self._isClickedDown = False
        self._LastPosition = self.GetPosition()

        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        # self.SetTitle("frame")
        size = (22, 22)
        if platform.system() == 'Linux':
            size = (32, 22)

        self.btnMinimize.SetMinSize(size)
        self.btnMinimize.SetBitmap(
            wx.Bitmap(os.path.join(self._exe_path, "img", "min.png"),
                      wx.BITMAP_TYPE_ANY))
        self.btnMaximize.SetMinSize(size)
        self.btnMaximize.SetBitmap(
            wx.Bitmap(os.path.join(self._exe_path, "img", "max.png"),
                      wx.BITMAP_TYPE_ANY))
        self.btnExit.SetMinSize(size)
        self.btnExit.SetBitmap(
            wx.Bitmap(os.path.join(self._exe_path, "img", "close.png"),
                      wx.BITMAP_TYPE_ANY))
        self.panelTitleBar.SetBackgroundColour(wx.Colour(44, 134, 179))
        self.panelBody.SetBackgroundColour(wx.Colour(255, 255, 255))

    def __do_layout(self):

        # Sizers:
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_1 = wx.FlexGridSizer(2, 1, 0, 0)
        sizerTitleBar = wx.FlexGridSizer(1, 4, 0, 0)

        body_sizer = wx.BoxSizer(wx.VERTICAL)
        body_sizer1 = wx.FlexGridSizer(4, 3, 30, 0)
        body_sizer2 = wx.BoxSizer(wx.HORIZONTAL)

        # Titlebar:
        bitmap = wx.Bitmap(os.path.join(
            self._exe_path, "img", "login_universal_copy_paste_tools.png"))

        iconTitleBar = wx.StaticBitmap(self.panelTitleBar, wx.ID_ANY,
                                       bitmap)

        sizerTitleBar.Add(iconTitleBar, 0,
                          wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 5)

        sizerTitleBar.Add(self.btnMinimize, 0,
                          wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 2)
        sizerTitleBar.Add(self.btnMaximize, 0,
                          wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 2)
        sizerTitleBar.Add(self.btnExit, 0,
                          wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 2)
        sizerTitleBar.AddGrowableRow(0)
        sizerTitleBar.AddGrowableCol(0)

        body_sizer1.Add(
            self.server, 1,
            wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 2)
        body_sizer1.Add(
            self.server_text, 1,
            wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        body_sizer1.Add(
            self.btn_sign_in, 1,
            wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        body_sizer1.Add(
            self.user, 1,
            wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 2)
        body_sizer1.Add(
            self.user_text, 1,
            wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        body_sizer1.Add(
            self.btn_sign_up, 1,
            wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        body_sizer1.Add(
            self.password, 1,
            wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 2)
        body_sizer1.Add(
            self.password_text, 1,
            wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        body_sizer1.Add(
            self.btn_sign_out, 1,
            wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        body_sizer1.Add(
            self.save_password, 1, wx.ALIGN_CENTER | wx.CENTER, 5)
        body_sizer1.Add(
            self.btn_forget_password, 1, wx.ALIGN_CENTER | wx.CENTER, 5)
        body_sizer1.Add(
            self.skybility_logo, 1, wx.ALIGN_CENTER | wx.CENTER, 5)

        body_sizer1.AddGrowableCol(2)
        body_sizer1.AddGrowableRow(3)
        body_sizer2.Add(body_sizer1,
                        flag=wx.ALIGN_CENTER_VERTICAL | wx.RIGHT | wx.LEFT)
        body_sizer.AddStretchSpacer(prop=1)
        body_sizer.Add(body_sizer2, 0, wx.CENTER)
        body_sizer.AddStretchSpacer(prop=1)

        self.panelTitleBar.SetSizer(sizerTitleBar)
        self.panelBody.SetSizer(body_sizer)

        grid_sizer_1.Add(self.panelTitleBar, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(self.panelBody, 1, wx.EXPAND, 0)
        grid_sizer_1.AddGrowableRow(1)
        grid_sizer_1.AddGrowableCol(0)
        sizer_1.Add(grid_sizer_1, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)

    def OnTitleBarLeftDown(self, event):
        self._LastPosition = event.GetPosition()

    def OnBtnExitClick(self, event):
        # self.Close()
        if not TaskBar.is_system_tray_available():
            wx.Exit()

        self.Hide()
        return False

    def OnBtnMinimizeClick(self, event):
        self.Iconize(True)

    def OnBtnMaximizeClick(self, event):
        self.Maximize(not self.IsMaximized())

    def OnMouseMove(self, event):
        if event.Dragging():
            mouse_x, mouse_y = wx.GetMousePosition()
            self.Move(mouse_x - self._LastPosition[0],
                      mouse_y - self._LastPosition[1])


class RegistUI(UI):
    def __init__(self, exe_path, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._exe_path = exe_path
        self.panelTitleBar = wx.Panel(self, wx.ID_ANY)
        self.btnMinimize = wx.Button(self.panelTitleBar, wx.ID_ANY, "",
                                     style=wx.BORDER_NONE | wx.BU_NOTEXT)
        self.btnMaximize = wx.Button(self.panelTitleBar, wx.ID_ANY, "",
                                     style=wx.BORDER_NONE | wx.BU_NOTEXT)

        self.btnExit = wx.Button(self.panelTitleBar, wx.ID_ANY, "",
                                 style=wx.BORDER_NONE | wx.BU_NOTEXT)
        self.panelBody = wx.Panel(self, wx.ID_ANY)

        self.Bind(wx.EVT_BUTTON, self.OnBtnExitClick, self.btnExit)
        self.Bind(wx.EVT_BUTTON, self.OnBtnMinimizeClick, self.btnMinimize)
        self.Bind(wx.EVT_BUTTON, self.OnBtnMaximizeClick, self.btnMaximize)
        self.panelTitleBar.Bind(wx.EVT_LEFT_DOWN, self.OnTitleBarLeftDown)
        self.panelTitleBar.Bind(wx.EVT_MOTION, self.OnMouseMove)

        self.user_name = wx.StaticText(self.panelBody, wx.ID_ANY,
                                       label="username: ")
        self.password = wx.StaticText(self.panelBody, wx.ID_ANY,
                                      label="password: ")
        self.repeat_pw = wx.StaticText(self.panelBody, wx.ID_ANY,
                                       label="repeatpw: ")

        self.username_text = wx.TextCtrl(self.panelBody, wx.ID_ANY,
                                         size=wx.Size(230, 40))
        self.username_text.SetBackgroundColour(wx.Colour(230, 230, 250))
        _font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.username_text.SetFont(_font)

        self.pw_text = wx.TextCtrl(self.panelBody, wx.ID_ANY,
                                   size=wx.Size(230, 40),
                                   style=wx.TE_PASSWORD)
        self.pw_text.SetBackgroundColour(wx.Colour(230, 230, 250))
        _font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.pw_text.SetFont(_font)

        self.repw_text = wx.TextCtrl(self.panelBody, wx.ID_ANY,
                                     size=wx.Size(230, 40),
                                     style=wx.TE_PASSWORD)
        self.repw_text.SetBackgroundColour(wx.Colour(230, 230, 250))
        _font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.repw_text.SetFont(_font)

        self.btn_ok = wx.Button(self.panelBody, wx.ID_ANY, label="OK",
                                size=(80, 38))
        self.btn_ok.SetBackgroundColour(wx.Colour(44, 134, 179))
        self.btn_ok.SetForegroundColour(wx.Colour(255, 255, 255))

        self._isClickedDown = False
        self._LastPosition = self.GetPosition()

        self.__set_properties()
        self.__do_layout()

        self.Centre()
        self.Show(True)

    def __set_properties(self):
        self.SetTitle("frame")
        size = (22, 22)
        if platform.system() == 'Linux':
            size = (32, 22)

        self.btnMinimize.SetMinSize(size)
        self.btnMinimize.SetBitmap(
            wx.Bitmap(os.path.join(self._exe_path, "img", "min.png"),
                      wx.BITMAP_TYPE_ANY))
        self.btnMaximize.SetMinSize(size)
        self.btnMaximize.SetBitmap(
            wx.Bitmap(os.path.join(self._exe_path, "img", "max.png"),
                      wx.BITMAP_TYPE_ANY))
        self.btnExit.SetMinSize(size)
        self.btnExit.SetBitmap(
            wx.Bitmap(os.path.join(self._exe_path, "img", "close.png"),
                      wx.BITMAP_TYPE_ANY))
        self.panelTitleBar.SetBackgroundColour(wx.Colour(44, 134, 179))
        self.panelBody.SetBackgroundColour(wx.Colour(255, 255, 255))

    def __do_layout(self):

        # Sizers:
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_1 = wx.FlexGridSizer(2, 1, 0, 0)
        sizerTitleBar = wx.FlexGridSizer(1, 4, 0, 0)

        body_sizer = wx.BoxSizer(wx.VERTICAL)
        body_sizer1 = wx.FlexGridSizer(4, 2, 30, 15)
        body_sizer2 = wx.BoxSizer(wx.HORIZONTAL)

        # Titlebar:
        bitmap = wx.Bitmap(os.path.join(self._exe_path,
                                        "img", "reg_registeruser.png"))

        iconTitleBar = wx.StaticBitmap(self.panelTitleBar, wx.ID_ANY,
                                       bitmap)

        sizerTitleBar.Add(iconTitleBar, 0,
                          wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 5)

        sizerTitleBar.Add(self.btnMinimize, 0,
                          wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 2)
        sizerTitleBar.Add(self.btnMaximize, 0,
                          wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 2)
        sizerTitleBar.Add(self.btnExit, 0,
                          wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 2)
        sizerTitleBar.AddGrowableRow(0)
        sizerTitleBar.AddGrowableCol(0)

        body_sizer1.Add(
            self.user_name, 1,
            wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 2)
        body_sizer1.Add(
            self.username_text, 1,
            wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        body_sizer1.Add(
            self.password, 1,
            wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        body_sizer1.Add(
            self.pw_text, 1,
            wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL,
            2)
        body_sizer1.Add(
            self.repeat_pw, 1,
            wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        body_sizer1.Add(
            self.repw_text, 1,
            wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        body_sizer1.AddStretchSpacer(prop=1)
        body_sizer1.Add(
            self.btn_ok, 1, wx.ALIGN_CENTER | wx.CENTER, 5)
        # body_sizer1.Add(
        #     self.skybility_logo, 1, wx.ALIGN_CENTER | wx.CENTER, 5)

        body_sizer1.AddGrowableCol(1)
        body_sizer1.AddGrowableRow(3)
        body_sizer2.Add(body_sizer1,
                        flag=wx.ALIGN_CENTER_VERTICAL | wx.RIGHT | wx.LEFT)
        body_sizer.AddStretchSpacer(prop=1)
        body_sizer.Add(body_sizer2, 0, wx.CENTER)
        body_sizer.AddStretchSpacer(prop=1)

        self.panelTitleBar.SetSizer(sizerTitleBar)
        self.panelBody.SetSizer(body_sizer)

        grid_sizer_1.Add(self.panelTitleBar, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(self.panelBody, 1, wx.EXPAND, 0)
        grid_sizer_1.AddGrowableRow(1)
        grid_sizer_1.AddGrowableCol(0)
        sizer_1.Add(grid_sizer_1, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)

    def OnTitleBarLeftDown(self, event):
        self._LastPosition = event.GetPosition()

    def OnBtnExitClick(self, event):
        self.Close()

    def OnBtnMinimizeClick(self, event):
        self.Iconize(True)

    def OnBtnMaximizeClick(self, event):
        self.Maximize(not self.IsMaximized())

    def OnMouseMove(self, event):
        if event.Dragging():
            mouse_x, mouse_y = wx.GetMousePosition()
            self.Move(mouse_x - self._LastPosition[0],
                      mouse_y - self._LastPosition[1])


class TaskBar:
    def __init__(self, system_tray):
        self.system_tray = system_tray

    @classmethod
    def is_system_tray_available(cls):
        bar = wx.adv.TaskBarIcon()
        return bar.IsAvailable()

    def create_menu_item(self, menu: wx.Menu, label, func):
        menu.AppendSeparator()
        item = wx.MenuItem(menu, -1, label)
        menu.Bind(wx.EVT_MENU, func, id=item.GetId())
        menu.Append(item)

        if label == "Start Service":
            item.Enable(self.system_tray.app.service_started is False)
        if label == "Stop Service":
            item.Enable(self.system_tray.app.service_started is True)

        return item

    def chk_item_click(self, menu, label, func, item_list=[]):
        menu.AppendSeparator()
        _menu = wx.Menu()
        if label == "Recent Content":
            for x in range(len(item_list)):
                client_1 = _menu.AppendCheckItem(wx.NewId(),
                                                 f'{x}: '
                                                 f'{item_list[x][21:31]}...')
                _menu.Bind(wx.EVT_MENU, func(x), id=client_1.GetId())

        elif label == "Client List":
            for x in item_list.current_clients:
                client_2 = _menu.AppendCheckItem(wx.NewId(), x)
                client_2.Check(x not in item_list.ignore_clients)
                _menu.Bind(wx.EVT_MENU, func(x), id=client_2.GetId())

        menu.Append(wx.ID_ANY, label, _menu)
