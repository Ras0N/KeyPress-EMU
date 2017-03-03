# -*- coding:GBK -*-

import os
import sys
import win32api
import ctypes
import _winreg
from KeyCode import *
class Basic:
    isAdmin = False
    def __init__(self):
        self.isAdmin = self.__bisAdmin()
    def __bisAdmin(self):
        hKey = (ctypes.wintypes.HKEY)()
        Advapi = ctypes.windll.LoadLibrary("Advapi32.dll")
        Advapi.RegOpenKeyExW.argtypes=[wintypes.ULONG,wintypes.LPCWSTR,wintypes.c_int,wintypes.DWORD,wintypes.c_void_p]
        bRes = Advapi.RegOpenKeyExW(_winreg.HKEY_LOCAL_MACHINE,r"Software\\Microsoft\\Windows NT\\CurrentVersion\\",0,_winreg.KEY_READ|_winreg.KEY_WRITE,byref(hKey))
        Advapi.RegCloseKey.argtypes=[wintypes.HKEY]
        Advapi.RegCloseKey(hKey)
        if bRes != 0:
            return False
        else :
            return True
class KeyFunction(Basic):
    def KeyPress(Key,count):
        for i in range(count):
            win32api.keybd_event(Key,0x45,KEYEVENTF_EXTENDEDKEY | 0,0);
            win32api.keybd_event(Key,0x45,KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP,0);
