// ���� ifdef ���Ǵ���ʹ�� DLL �������򵥵�
// ��ı�׼�������� DLL �е������ļ��������������϶���� SCREENFUNCTION_EXPORTS
// ���ű���ġ���ʹ�ô� DLL ��
// �κ�������Ŀ�ϲ�Ӧ����˷��š�������Դ�ļ��а������ļ����κ�������Ŀ���Ὣ
// SCREENFUNCTION_API ������Ϊ�Ǵ� DLL ����ģ����� DLL ���ô˺궨���
// ������Ϊ�Ǳ������ġ�
#ifdef SCREENFUNCTION_EXPORTS
#define SCREENFUNCTION_API extern "C" __declspec(dllexport)
#else
#define SCREENFUNCTION_API __declspec(dllimport)
#endif

#define PYDLL __stdcall

/*
// �����Ǵ� ScreenFunction.dll ������
class SCREENFUNCTION_API CScreenFunction {
public:
	CScreenFunction(void);
	// TODO:  �ڴ�������ķ�����
};

extern SCREENFUNCTION_API int nScreenFunction;

SCREENFUNCTION_API int fnScreenFunction(void);
*/
SCREENFUNCTION_API DWORD32 PYDLL GetWindowPixel(HWND hWnd, int x, int y);
SCREENFUNCTION_API HBITMAP PYDLL GetWindowImg(HWND hWnd);
SCREENFUNCTION_API int PYDLL GetWindowMultiPixel(HWND hWnd, PINT PosArr, PDWORD32 pRGB);