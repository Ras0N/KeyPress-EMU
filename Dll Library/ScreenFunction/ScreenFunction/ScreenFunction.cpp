// ScreenFunction.cpp : 定义 DLL 应用程序的导出函数。
//

#include "stdafx.h"
#include "ScreenFunction.h"

#include <stdlib.h>
#include <malloc.h>
#include <Windows.h>
#include <WinUser.h>
#include <wingdi.h>
//#include <afxwin.h>

/*
// 这是导出变量的一个示例
SCREENFUNCTION_API int nScreenFunction=0;

// 这是导出函数的一个示例。
SCREENFUNCTION_API int fnScreenFunction(void)
{
    return 42;
}

// 这是已导出类的构造函数。
// 有关类定义的信息，请参阅 ScreenFunction.h
CScreenFunction::CScreenFunction()
{
    return;
}
*/
SCREENFUNCTION_API HBITMAP PYDLL GetWindowImg(HWND hWnd)
{
	HDC dcSrc = GetWindowDC(hWnd);
	RECT wRect = { 0, };
	GetWindowRect(hWnd, &wRect);
	long dwWidth = wRect.right - wRect.left;
	long dwHigh = wRect.bottom - wRect.top;
	HDC dcDest = CreateCompatibleDC(dcSrc);
	HBITMAP hBitmap = CreateCompatibleBitmap(dcSrc, dwWidth, dwHigh);
	HGDIOBJ hObj = SelectObject(dcDest, hBitmap);
	if (!BitBlt(dcDest, 0, 0, dwWidth, dwHigh, dcSrc, 0, 0, SRCCOPY))
	{
		OutputDebugString(L"Error While Copy Image!");
	}
	SelectObject(dcDest, hObj);
	DeleteDC(dcDest);
	ReleaseDC(hWnd, dcSrc);

	return hBitmap;
}

SCREENFUNCTION_API int PYDLL GetWindowMultiPixel(HWND hWnd, PINT PosArr, PDWORD32 pRGB)
{
	//PosArr end with 0
	if (PosArr == NULL)
		return 0;
	int bufferlen = 0;
	while (*(PosArr + bufferlen))
		bufferlen++;
	if (pRGB == NULL)
	{
		return (bufferlen + 2)/2;
	}
	int x, y;
	x = 0;
	y = 0;
	HBITMAP m_bmp = GetWindowImg(hWnd);
	BITMAP bmp;
	GetObject(m_bmp, sizeof(BITMAP), &bmp);
	//CBitmap m_bmp;
	//m_bmp.GetBitmap(&bmp);
	HDC hdc = GetDC(NULL);
	PBYTE pBits = NULL;
	BITMAPINFO bi = { 0, };
	bi.bmiHeader.biSize = sizeof(bi.bmiHeader);
	bi.bmiHeader.biWidth = bmp.bmWidth;
	bi.bmiHeader.biHeight = -bmp.bmHeight;
	bi.bmiHeader.biPlanes = 1;
	bi.bmiHeader.biBitCount = bmp.bmBitsPixel;
	bi.bmiHeader.biCompression = BI_RGB;
	//bi.bmiHeader.biSizeImage = bmp.bmWidth * bmp.bmHeight * nByte;
	bi.bmiHeader.biClrUsed = 0;
	bi.bmiHeader.biClrImportant = 0;
	if (!GetDIBits(hdc, m_bmp, 0, bmp.bmHeight, pBits, &bi, DIB_RGB_COLORS))
	{
		OutputDebugString(L"Error While Get Header Size");
		return 0;
	}
	pBits = (PBYTE)malloc(bi.bmiHeader.biSizeImage);
	ZeroMemory(pBits, bi.bmiHeader.biSizeImage);
	if (!GetDIBits(hdc, m_bmp, 0, bmp.bmHeight, pBits, &bi, DIB_RGB_COLORS))
	{
		free(pBits);
		pBits = NULL;
	}
	for (int i = 0; i < bufferlen >> 1; i++)
	{
		x = *(PosArr + 2 * i);
		y = *(PosArr + 2 * i + 1);
		int offset = (y - 1)*bmp.bmWidth + x - 1;//可能越界 添加越界检查
		DWORD32 RGB = 0;
		if (offset > bi.bmiHeader.biSizeImage >> 2 || offset < 0) {
			RGB = 0;
			OutputDebugString(L"Access Violation!");
		}
		else
			RGB = *((PDWORD32)(pBits)+offset);
		*(pRGB + i) = RGB;
	}
	free(pBits);
	pBits = NULL;
	return 1;
}

SCREENFUNCTION_API DWORD32 PYDLL GetWindowPixel(HWND hWnd,int x, int y) {
	HBITMAP m_bmp = GetWindowImg(hWnd);
	BITMAP bmp;
	GetObject(m_bmp, sizeof(BITMAP), &bmp);
	//CBitmap m_bmp;
	//m_bmp.GetBitmap(&bmp);
	HDC hdc = GetDC(NULL);
	PBYTE pBits = NULL;
	BITMAPINFO bi = { 0, };
	bi.bmiHeader.biSize = sizeof(bi.bmiHeader);
	bi.bmiHeader.biWidth = bmp.bmWidth;
	bi.bmiHeader.biHeight = -bmp.bmHeight;
	bi.bmiHeader.biPlanes = 1;
	bi.bmiHeader.biBitCount = bmp.bmBitsPixel;
	bi.bmiHeader.biCompression = BI_RGB;
	//bi.bmiHeader.biSizeImage = bmp.bmWidth * bmp.bmHeight * nByte;
	bi.bmiHeader.biClrUsed = 0;
	bi.bmiHeader.biClrImportant = 0;
	if (!GetDIBits(hdc, m_bmp, 0, bmp.bmHeight, pBits, &bi, DIB_RGB_COLORS))
	{
		OutputDebugString(L"Error While Get Header Size");
		return 0;
	}
	pBits = (PBYTE)malloc(bi.bmiHeader.biSizeImage);
	ZeroMemory(pBits, bi.bmiHeader.biSizeImage);
	if (!GetDIBits(hdc, m_bmp, 0, bmp.bmHeight, pBits, &bi, DIB_RGB_COLORS))
	{
		free(pBits);
		pBits = NULL;
	}
	int offset = (y - 1)*bmp.bmWidth + x - 1;//可能越界 添加越界检查
	DWORD32 RGB = 0;
	if (offset > bi.bmiHeader.biSizeImage >> 2 || offset < 0) {
		RGB = 0;
		OutputDebugString(L"Access Violation!");
	}
	else
		RGB = *((PDWORD32)(pBits)+offset);
	free(pBits);
	pBits = NULL;
	return RGB;
}
