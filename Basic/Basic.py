# -*- coding:GBK -*-

import os
import sys
import win32api
import ctypes
from KeyCode import *
class Basic:
    isAdmin = False
    class SID_IDENTIFIER_AUTHORITY(Structure):
        _fields_ = {("Value",ctypes.wintypes.BYTE * 6)}
    def __init__():
        isAdmin = False
    def isAdmin():
        #from http://bbs.csdn.net/topics/391025033
        hAccessToken = 0
        InfoBuffer = None
        ptgGroups = None
        dwInfoBufferSize = 0
        psidAdministrators = None
        siaNtAuthority = SID_IDENTIFIER_AUTHORITY()
        i = 0
        bRet = False
        
class KeyFunction(Basic):
    def KeyPress(Key,count):
        for i in range(count):
            win32api.keybd_event(Key,0x45,KEYEVENTF_EXTENDEDKEY | 0,0);
            win32api.keybd_event(Key,0x45,KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP,0);
