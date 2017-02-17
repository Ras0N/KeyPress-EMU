// 下列 ifdef 块是创建使从 DLL 导出更简单的
// 宏的标准方法。此 DLL 中的所有文件都是用命令行上定义的 SCREENFUNCTION_EXPORTS
// 符号编译的。在使用此 DLL 的
// 任何其他项目上不应定义此符号。这样，源文件中包含此文件的任何其他项目都会将
// SCREENFUNCTION_API 函数视为是从 DLL 导入的，而此 DLL 则将用此宏定义的
// 符号视为是被导出的。
#ifdef SCREENFUNCTION_EXPORTS
#define SCREENFUNCTION_API extern "C" __declspec(dllexport)
#else
#define SCREENFUNCTION_API __declspec(dllimport)
#endif

#define PYDLL __stdcall

/*
// 此类是从 ScreenFunction.dll 导出的
class SCREENFUNCTION_API CScreenFunction {
public:
	CScreenFunction(void);
	// TODO:  在此添加您的方法。
};

extern SCREENFUNCTION_API int nScreenFunction;

SCREENFUNCTION_API int fnScreenFunction(void);
*/
SCREENFUNCTION_API DWORD32 PYDLL GetWindowPixel(HWND hWnd, int x, int y);
SCREENFUNCTION_API HBITMAP PYDLL GetWindowImg(HWND hWnd);
SCREENFUNCTION_API int PYDLL GetWindowMultiPixel(HWND hWnd, PINT PosArr, PDWORD32 pRGB);