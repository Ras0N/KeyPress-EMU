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
    def __init__(self):
        Basic.__init__(self)
        if self.isAdmin == False:
            print "[*][WARING] You're not running this script as Administrator,some function may not work properly."
    def Ascii2VirtualKey(self,Key):
        return win32api.VkKeyScan(Key)
    def KeyPress(self,Key,count = 1):
        if  isinstance(Key,str) and len(Key) == 1:
            Key = self.Ascii2VirtualKey(Key)
        elif not isinstance(Key,int):
            print "[*][Err] Type Error!"
            return
        for i in range(count):
            win32api.keybd_event(Key,0x45,KEYEVENTF_EXTENDEDKEY | 0,0);
            win32api.keybd_event(Key,0x45,KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP,0);
    def KeyHold(self,Key):
        if  isinstance(Key,str) and len(Key) == 1:
            Key = self.Ascii2VirtualKey(Key)
        elif not isinstance(Key,int):
            print "[*][Err] Type Error!"
            return
        win32api.keybd_event(Key,0x45,KEYEVENTF_EXTENDEDKEY | 0,0);
        #win32api.keybd_event(Key,0x45,KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP,0);
    def KeyRelease(self,Key):
        if  isinstance(Key,str) and len(Key) == 1:
            Key = self.Ascii2VirtualKey(Key)
        elif not isinstance(Key,int):
            print "[*][Err] Type Error!"
            return
        #win32api.keybd_event(Key,0x45,KEYEVENTF_EXTENDEDKEY | 0,0);
        win32api.keybd_event(Key,0x45,KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP,0);        