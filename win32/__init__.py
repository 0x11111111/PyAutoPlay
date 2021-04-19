# -*- coding:utf-8 -*-

import base64
import ctypes
import datetime
import os
import re
import sys
import time
from io import BytesIO, TextIOWrapper
import pyscreeze
import win32api
import win32con
import win32gui
import win32ui
from PIL import Image
from .utils import PAGException
from typing import Union, Optional, Any

__key={
    'mouse_left':[win32con.WM_LBUTTONDOWN,win32con.WM_LBUTTONUP,win32con.MK_LBUTTON],
    'mouse_middle':[win32con.WM_MBUTTONDOWN,win32con.WM_MBUTTONUP,win32con.MK_MBUTTON],
    'mouse_right':[win32con.WM_RBUTTONDOWN,win32con.WM_RBUTTONUP,win32con.MK_RBUTTON],
    'kb_shift':[win32con.MK_SHIFT],
}

class PyAutoPlay_win32:
    """base class"""
    def __init__(self):
        self.img_type = 'JPG'
        self.left = 0
        self.right = 0
        self.bottom = 0
        self.top = 0
        self.width = 0
        self.height = 0
        self.x = 0
        self.y = 0
        self.hwnd = None
        self.title = ''

    def set_hwnd(self, hwnd: Optional[int]) -> None:
        self.hwnd = hwnd

    def sleep(self, _time: Optional[int]) -> None:
        return time.sleep(_time)

    def images(self, *_image_list, prefix=None):
        """
        Full name of image files like 
         ['D://img1.jpg','D://img2.jpg'] 
          OR
         ['img1.jpg','img2.jpg'] with prefix='D://'
        """
        pass

    def get_all_hwnd_title(self) -> dict:
        '''return a dict contains all hwnd and title'''
        hwnd_title = dict()

        def get_all_hwnd(hwnd, mouse):
            if (
                win32gui.IsWindow(hwnd)
                and win32gui.IsWindowEnabled(hwnd)
                and win32gui.IsWindowVisible(hwnd)
            ):
                hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})
        win32gui.EnumWindows(get_all_hwnd, 0)
        return hwnd_title

    def find_title_custom(self, window_name: Optional[str]) -> dict:
        ''' find_title_custom'''
        self.title = window_name
        hwnd_title = self.get_all_hwnd_title()
        match_hwnd_title = dict()
        for h, t in hwnd_title.items():
            if window_name in t:
                match_hwnd_title.update({h: t})
        return match_hwnd_title

    def find_title(self, window_name: Optional[str]) -> int:
        ''' return the first match hwnd(int) '''
        hwnd_title = self.find_title_custom(window_name)
        for h, t in hwnd_title.items():
            if window_name in t:
                return int(h)
        raise PAGException("ERROR: title '{0}' not found!".format(window_name))

    def find_all_title(self, window_name: Optional[str]) -> dict:
        """return a dict contains all matched hwnd and title"""
        if m_h_t := self.find_title_custom(window_name) != {}:
            return m_h_t
        raise PAGException("ERROR: title '{0}' not found!".format(window_name))

    def get_screenshot(self) -> Image.Image:
        '''return a Image object'''
        hwnd = int(self.hwnd)
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        width = right - left
        height = bottom - top
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
        self.height = height
        self.width = width
        hWndDC = win32gui.GetWindowDC(hwnd)
        mfcDC = win32ui.CreateDCFromHandle(hWndDC)
        saveDC = mfcDC.CreateCompatibleDC()
        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
        saveDC.SelectObject(saveBitMap)
        saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)
        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)
        im_PIL = Image.frombuffer(
            "RGB",
            (bmpinfo["bmWidth"], bmpinfo["bmHeight"]),
            bmpstr,
            "raw",
            "BGRX",
            0,
            1,
        )
        return im_PIL

    def locate(self, image, type='', **kwargs):
        if type == "base64":
            needle_image = BytesIO(base64.b64decode(image))
        else:
            needle_image = Image.open(image)

        haystack_image = self.get_screenshot()

        if res := pyscreeze.locate(needle_image, haystack_image) != None:
            position = []
            self.x = pyscreeze.center(res)[0]
            self.y = pyscreeze.center(res)[1]
            position.append(pyscreeze.center(res)[0])
            position.append(pyscreeze.center(res)[1])
            return True
        return False

    def click_custom(self, pos: Optional[list], key: Optional[str] = 'mouse_left', hold_time=0.05):
        ''' click custom'''
        _pos = win32api.MAKELONG(pos[0], pos[1])
        if key in ['mouse_left','mouse_middle','mouse_right']:
            _key=__key['key']
        else:
            raise PAGException("key {0} not found, please check available list".format(key))
        
        win32gui.SendMessage(self.hwnd, _key[0], win32con.WA_ACTIVE, 0)
        win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN,win32con.MK_LBUTTON, _pos)
        self.sleep(hold_time)
        win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, _pos)

    def sendkey(self, image, key: str, times=1, interval=0.1):
        """
        Send specified key to the matched image.

        Parameter:
            - image: image to be matched
            - key: send mouse click or press from keyboard
            - times: click times
        """
        pass

    def sendkeys(self, *_image_list: list, key: str, times=1, interval=0.1):
        """
        Send same key to all matched images.

        Parameter:
            - _image_list: list of images
            - key: send mouse click or press sth
            - times: each matched image click frequency
            - interval: send key interval
        """

        pass
