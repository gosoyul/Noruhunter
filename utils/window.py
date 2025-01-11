import ctypes

import numpy as np
from PIL import ImageGrab

# 아이콘 상수
MB_ICONERROR = 0x10         # ❌ 오류 아이콘
MB_ICONWARNING = 0x30       # ⚠ 경고 아이콘
MB_ICONINFORMATION = 0x40   # ℹ 정보 아이콘
MB_ICONQUESTION = 0x20      # ❓ 질문 아이콘

# 버튼 상수
MB_OK = 0x00                # [확인] 버튼
MB_OKCANCEL = 0x01          # [확인] [취소] 버튼
MB_YESNO = 0x04             # [예] [아니오] 버튼
MB_YESNOCANCEL = 0x03       # [예] [아니오] [취소] 버튼
MB_RETRYCANCEL = 0x05       # [다시 시도] [취소] 버튼
MB_ABORTRETRYIGNORE = 0x02  # [중지] [다시 시도] [무시] 버튼

def find_window(title):
    """윈도우 핸들 찾기"""
    return ctypes.windll.user32.FindWindowW(0, title)


def activate_window(hwnd=None, title=None):
    """윈도우 활성화"""
    if not hwnd:
        hwnd = find_window(title)

    ctypes.windll.user32.SetForegroundWindow(hwnd)


def get_client_rect(hwnd=None, title=None):
    """클라이언트 영역 가져오기"""

    if not hwnd:
        hwnd = find_window(title)

    # RECT 구조체 정의
    class RECT(ctypes.Structure):
        _fields_ = [("left", ctypes.c_long),
                    ("top", ctypes.c_long),
                    ("right", ctypes.c_long),
                    ("bottom", ctypes.c_long)]

    rect = RECT()  # RECT 구조체 인스턴스를 생성
    ctypes.windll.user32.GetClientRect(hwnd, ctypes.byref(rect))  # RECT 구조체를 채움
    return rect.left, rect.top, rect.right - rect.left, rect.bottom - rect.top


def client_to_screen(client_x, client_y, hwnd=None, window_title=None):
    """클라이언트 좌표를 스크린 좌표로 변환하기"""

    if not hwnd:
        hwnd = find_window(window_title)

    # POINT 구조체 정의
    class POINT(ctypes.Structure):
        _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

    point = POINT(client_x, client_y)

    # ClientToScreen 함수 호출
    ctypes.windll.user32.ClientToScreen(hwnd, ctypes.byref(point))

    return point.x, point.y


def get_client_area(hwnd=None, window_title=None):
    """win32gui를 사용하여 윈도우의 클라이언트 영역의 좌표와 크기 구하기"""
    if not hwnd:
        hwnd = find_window(window_title)

    client_x, client_y, client_width, client_height = get_client_rect(hwnd)  # 클라이언트 영역
    screen_x, screen_y = client_to_screen(client_x, client_y, hwnd)

    center_x, center_y = screen_x + client_width // 2, screen_y + client_height // 2

    return screen_x, screen_y, client_width, client_height, center_x, center_y


def show_message(title, message, with_cancel=False, icon=MB_ICONINFORMATION):
    """메시지박스를 띄우는 함수"""
    return ctypes.windll.user32.MessageBoxW(0, message, title, icon if with_cancel else 0x40)  # 0x40: 아이콘, 0x1: OK 버튼


def screenshot(rect_ratio, hwnd=None, window_title=None):
    """동적으로 설정된 비율을 적용하여 스크린샷을 찍는 함수"""
    if not hwnd:
        hwnd = find_window(window_title)

    client_x, client_y, client_width, client_height, _, _ = get_client_area(hwnd)
    _, left_ratio, right_ratio, top_ratio, bottom_ratio, _ = rect_ratio

    left = client_x + int(client_width * left_ratio)
    top = client_y + int(client_width * top_ratio)
    right = client_x + client_width - int(client_width * left_ratio * 2)
    bottom = client_y + client_height - int(client_width * bottom_ratio)

    print(f"📸 Left: {left}, Top: {top}, Right: {right}, Bottom: {bottom}")

    return np.array(ImageGrab.grab(bbox=(left, top, right, bottom)))
