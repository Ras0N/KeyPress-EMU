# -*- coding:GBK -*-

import ctypes
import os
import math
import time
import win32api
from ctypes import wintypes
from ctypes import *

NULL = 0

User32 = ctypes.windll.LoadLibrary("User32.dll")
Kernel32 = ctypes.windll.LoadLibrary("Kernel32.dll")
Gdi32 = ctypes.windll.LoadLibrary("Gdi32.dll")

class CRECT(Structure):
    _fields_ = [ ("left",c_long),
                 ("top",c_long),
                 ("right",c_long),
                 ("bottom",c_long)]
    
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010

class cPOS:
    x = 0
    y = 0
    
def SetCursePos(x,y):
    User32.SetCursorPos.argtypes=[ctypes.wintypes.c_int,ctypes.wintypes.c_int]
    User32.SetCursorPos(int(x),int(y))
    
def EmuCursorEvent(x,y,event,Abs):
    User32.mouse_event.argtypes=[ctypes.wintypes.DWORD,
                                 ctypes.wintypes.DWORD,
                                 ctypes.wintypes.DWORD,
                                 ctypes.wintypes.DWORD,
                                 ctypes.wintypes.c_void_p]#ULONG_PTR
    if Abs:
        User32.mouse_event(event|0x8000,x,y,0,None)
    else:
        User32.mouse_event(event,x,y,0,None)
        
def EmuCursorClick(x,y):
    SetCursePos(x,y)
    #EmuCursorEvent(x,y,MOUSEEVENTF_LEFTDOWN|MOUSEEVENTF_LEFTUP,True)
    EmuCursorEvent(0,0,MOUSEEVENTF_LEFTDOWN,False)
    time.sleep(0.01)
    EmuCursorEvent(0,0,MOUSEEVENTF_LEFTUP,False)
    
def main():
    wHWND = None
    #szName = create_string_buffer("计算器")
    User32.FindWindowW.argtypes=[ctypes.wintypes.LPCWSTR,ctypes.wintypes.LPCWSTR]
    User32.FindWindowW.restypes=ctypes.wintypes.HWND
    wHWND = User32.FindWindowW(None,'Bluestacks App Player')
    #wHWND = User32.FindWindowW(None,"计算器")
    if wHWND == NULL:
        print 'error'
        print Kernel32.GetLastError()
        exit(1)
    else:
        print wHWND
    User32.IsWindowVisible.argtypes=[ctypes.wintypes.HWND]
    if not User32.IsWindowVisible(wHWND):
        print "窗口未置顶"
        exit(1)
        
    rect = CRECT()
    User32.GetWindowRect.argtypes=[ctypes.wintypes.HWND,ctypes.wintypes.c_void_p]
    if not User32.GetWindowRect(wHWND,byref(rect)):
        exit(1)
    dwHigh = rect.bottom-rect.top
    dwWide = rect.right-rect.left
    
    WindowFunction = ctypes.windll.LoadLibrary("ScreenFunction.dll")
    DllGetPixel = WindowFunction.GetWindowPixel
    DllGetPixel.argtypes=[ctypes.wintypes.HWND,ctypes.wintypes.c_int,ctypes.wintypes.c_int]
    DllGetPixel.restypes=[ctypes.wintypes.c_uint32]
    DllGetMultiPixel = WindowFunction.GetWindowMultiPixel
    DllGetMultiPixel.argtypes=[ctypes.wintypes.HWND,ctypes.wintypes.c_void_p,ctypes.wintypes.c_void_p]
    DllGetMultiPixel.restypes=[ctypes.wintypes.c_int]
    #Pos(0).x = dwHigh * 0.13
    Pos0 = cPOS()
    Pos1 = cPOS()
    Pos2 = cPOS()
    Pos3 = cPOS()
    Pos0.y = int(math.floor(dwHigh * 0.64))
    Pos1.y = int(math.floor(dwHigh * 0.64))
    Pos2.y = int(math.floor(dwHigh * 0.64))
    Pos3.y = int(math.floor(dwHigh * 0.64))
    Pos0.x = int(math.floor(dwWide * 0.13))
    Pos1.x = int(math.floor(dwWide * 0.37))
    Pos2.x = int(math.floor(dwWide * 0.62))
    Pos3.x = int(math.floor(dwWide * 0.86))   
    #print hex(RGB0&0xFFFFFFFF)
    #print hex(RGB1&0xFFFFFFFF)
    #print hex(RGB2&0xFFFFFFFF)
    #print hex(RGB3&0xFFFFFFFF)
    #SetCursePos(rect.left+Pos0.x,rect.top+Pos0.y)
    #EmuCursorClick(rect.left+Pos0.x,rect.top+Pos0.y)
    cMulti = (ctypes.wintypes.c_int * 17)(Pos0.x,Pos0.y,Pos1.x,Pos1.y,Pos2.x,Pos2.y,Pos3.x,Pos3.y,
                                         Pos0.x,Pos0.y-5,Pos1.x,Pos1.y-5,Pos2.x,Pos2.y-5,Pos3.x,Pos3.y-5,
                                         0)
    dwLen = DllGetMultiPixel(wHWND,byref(cMulti),None)
    RGB = (ctypes.wintypes.DWORD * dwLen)()
    quit = False
    while not quit:
        #RGB0 = DllGetPixel(wHWND,Pos0.x,Pos0.y) & 0xffffffff
        #RGB1 = DllGetPixel(wHWND,Pos1.x,Pos1.y) & 0xffffffff
        #RGB2 = DllGetPixel(wHWND,Pos2.x,Pos2.y) & 0xffffffff
        #RGB3 = DllGetPixel(wHWND,Pos3.x,Pos3.y) & 0xffffffff
        DllGetMultiPixel(wHWND,byref(cMulti),byref(RGB))
        #RGB4 = DllGetPixel(wHWND,Pos0.x,Pos0.y-5) & 0xffffffff
        #RGB5 = DllGetPixel(wHWND,Pos1.x,Pos1.y-5) & 0xffffffff
        #RGB6 = DllGetPixel(wHWND,Pos2.x,Pos2.y-5) & 0xffffffff
        #RGB7 = DllGetPixel(wHWND,Pos3.x,Pos3.y-5) & 0xffffffff        
        flag = 0
        if not RGB[0] == 0xfff5f5f5 or not RGB[4] == 0xfff5f5f5:#== 0xff202020 or RGB0 == 0xffd2d2d2:
            EmuCursorClick(rect.left+Pos0.x,rect.top+Pos0.y)
            flag = 1
        elif not RGB[1] == 0xfff5f5f5 or not RGB[5] == 0xfff5f5f5:# == 0xff202020 or RGB1 == 0xffd2d2d2:
            EmuCursorClick(rect.left+Pos1.x,rect.top+Pos1.y)
            flag = 2
        elif not RGB[2] == 0xfff5f5f5 or not RGB[6] == 0xfff5f5f5:#== 0xff202020 or RGB2 == 0xffd2d2d2:
            EmuCursorClick(rect.left+Pos2.x,rect.top+Pos2.y)
            flag = 3
        elif not RGB[3] == 0xfff5f5f5 or not RGB[7] == 0xfff5f5f5:#== 0xff202020 or RGB3 == 0xffd2d2d2:
            EmuCursorClick(rect.left+Pos3.x,rect.top+Pos3.y)
            flag = 4
        cot = 0
        if flag == 0:
            quit=True
        elif flag == 1:
            RGB0 = DllGetPixel(wHWND,Pos0.x,Pos0.y) & 0xffffffff
            while not RGB0 == 0xfff5f5f5:#== 0xff202020 or RGB0 == 0xffd2d2d2 or RGB0 == 0xff7a7a7a or RGB0 == 0xff454545:
                time.sleep(0.05)
                cot += 1
                if cot > 20:
                    quit=True
                    break                
                RGB0 = DllGetPixel(wHWND,Pos0.x,Pos0.y) & 0xffffffff
        elif flag == 2:        
            RGB1 = DllGetPixel(wHWND,Pos1.x,Pos1.y) & 0xffffffff
            while not RGB1 == 0xfff5f5f5:#== 0xff202020 or RGB1 == 0xffd2d2d2 or RGB1 == 0xff7a7a7a or RGB1 == 0xff454545:
                time.sleep(0.05)
                cot += 1
                if cot > 20:
                    quit=True
                    break
                RGB1 = DllGetPixel(wHWND,Pos1.x,Pos1.y) & 0xffffffff
        elif flag == 3:
            RGB2 = DllGetPixel(wHWND,Pos2.x,Pos2.y) & 0xffffffff
            while not RGB2 == 0xfff5f5f5:#== 0xff202020 or RGB2 == 0xffd2d2d2 or RGB2 == 0xff7a7a7a or RGB2 == 0xff454545:
                time.sleep(0.05)
                cot += 1
                if cot > 20:
                    quit=True
                    break                
                RGB2 = DllGetPixel(wHWND,Pos2.x,Pos2.y) & 0xffffffff
        elif flag == 4:
            RGB3 = DllGetPixel(wHWND,Pos3.x,Pos3.y) & 0xffffffff
            while not RGB3 == 0xfff5f5f5:#== 0xff202020 or RGB3 == 0xffd2d2d2 or RGB3 == 0xff7a7a7a or RGB3 == 0xff454545:
                time.sleep(0.05)
                cot += 1
                if cot > 20:
                    quit=True
                    break                
                RGB3 = DllGetPixel(wHWND,Pos3.x,Pos3.y) & 0xffffffff   
    print 'end'
if __name__=="__main__":
    main()