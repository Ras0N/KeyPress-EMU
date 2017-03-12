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
        #需要实现查询按键状况的代码 
        
class MouseFunction(Basic):
    def __init__(self):
        Basic.__init__(self)
        if self.isAdmin == False:
            print "[*][WARING] You're not running this script as Administrator,some function may not work properly."
        User32 = ctypes.windll.LoadLibrary("User32.dll")
        Kernel32 = ctypes.windll.LoadLibrary("Kernel32.dll")
        Gdi32 = ctypes.windll.LoadLibrary("Gdi32.dll")        
    def SetCursePos(self,x,y):
        User32.SetCursorPos.argtypes=[ctypes.wintypes.c_int,ctypes.wintypes.c_int]
        User32.SetCursorPos(int(x),int(y))
    def EmuCursorEvent(self,x,y,event,Abs=False):
        User32.mouse_event.argtypes=[ctypes.wintypes.DWORD,
                                     ctypes.wintypes.DWORD,
                                     ctypes.wintypes.DWORD,
                                     ctypes.wintypes.DWORD,
                                     ctypes.wintypes.c_void_p]#ULONG_PTR
        if Abs:
            User32.mouse_event(event|0x8000,x,y,0,None)
        else:
            User32.mouse_event(event,x,y,0,None)
    def EmuCursorClick(self,x=0,y=0,count=1,idelay=0.01):
        if not x == 0 and not y == 0:
            self.SetCursePos(x,y)
        #EmuCursorEvent(x,y,MOUSEEVENTF_LEFTDOWN|MOUSEEVENTF_LEFTUP,True)
        if idelay > 0:
            for i in range(count):
                self.EmuCursorEvent(0,0,MOUSEEVENTF_LEFTDOWN,False)
                time.sleep(idelay)
                self.EmuCursorEvent(0,0,MOUSEEVENTF_LEFTUP,False)
        else:
            for i in range(count):
                EmuCursorEvent(x,y,MOUSEEVENTF_LEFTDOWN|MOUSEEVENTF_LEFTUP,True)
#    def EmuCursorClickwithoutDelay(self,x,y,count=1):
 #       self.SetCursePos(x,y)
  #      for i in range(count):
   #         self.EmuCursorEvent(x,y,MOUSEEVENTF_LEFTDOWN|MOUSEEVENTF_LEFTUP,False)
    def EmuCursorLeftKeyDown(self,x=0,y=0):
        if x == 0 and y == 0:
            self.EmuCursorEvent(0,0,MOUSEEVENTF_LEFTDOWN,False)
        else:
            self.SetCursePos(x,y)
            self.EmuCursorEvent(0,0,MOUSEEVENTF_LEFTDOWN,False)
    def EmuCursorRightKeyDown(self,x=0,y=0):
        if x == 0 and y == 0:
            self.EmuCursorEvent(0,0,MOUSEEVENTF_RIGHTDOWN,False)
        else:
            self.SetCursePos(x,y)
            self.EmuCursorEvent(0,0,MOUSEEVENTF_RIGHTDOWN,False)
    def EmuCursorLeftKeyUp(self,x=0,y=0):
        if x == 0 and y == 0:
            self.EmuCursorEvent(0,0,MOUSEEVENTF_LEFTUP,False)
        else:
            self.SetCursePos(x,y)
            self.EmuCursorEvent(0,0,MOUSEEVENTF_LEFTUP,False)
    def EmuCursorRightKeyUp(self,x=0,y=0):
        if x == 0 and y == 0:
            self.EmuCursorEvent(0,0,MOUSEEVENTF_RIGHTUP,False)
        else:
            self.SetCursePos(x,y)
            self.EmuCursorEvent(0,0,MOUSEEVENTF_RIGHTUP,False)    
    def EmuCursorLeftDoubleClick(self,x=0,y=0):
        if x == 0 and y == 0:
            self.EmuCursorClick(x,y)
        else:
            self.SetCursePos(x,y)
            self.EmuCursorEvent(0,0,MOUSEEVENTF_RIGHTUP,False)        