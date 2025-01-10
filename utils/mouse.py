import ctypes
import time


# 마우스 위치를 지정된 좌표로 이동
def move_mouse(x, y):
    ctypes.windll.user32.SetCursorPos(x, y)


# 마우스 스크롤을 제어 (스크롤 방향: 양수는 위로, 음수는 아래로)
def scroll_mouse(delta):
    # MOUSEEVENTF_WHEEL (0x0800) - 스크롤 이벤트 발생
    ctypes.windll.user32.mouse_event(0x0800, 0, 0, delta, 0)


# 마우스 클릭 (왼쪽 버튼)
def click_mouse():
    # MOUSEEVENTF_LEFTDOWN (0x02) - 마우스 왼쪽 버튼 누르기
    # MOUSEEVENTF_LEFTUP (0x04) - 마우스 왼쪽 버튼 떼기
    ctypes.windll.user32.mouse_event(0x02, 0, 0, 0, 0)
    ctypes.windll.user32.mouse_event(0x04, 0, 0, 0, 0)


def scroll_down(count):
    for _ in range(count):
        # mouse.scroll(0, -1)
        scroll_mouse(-1)
        time.sleep(0.01)
