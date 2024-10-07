import win32gui
import win32con
import threading
import numpy as np
import time
import cv2
import pyautogui



def set_window_size(hwnd, width, height):
    # Get current window position
    rect = win32gui.GetWindowRect(hwnd)
    x, y = rect[0], rect[1]  # Current position

    # Set new width and height
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, x, y, width, height, win32con.SWP_NOZORDER)

# Sử dụng hàm và in ra kết quả
def findmap(frame1,y_them):
    hsv = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([40, 255, 255])
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rectangles = []

    # Vẽ các hình chữ nhật bao quanh các contour
    for contour in contours:
        # Tính toán hình chữ nhật bao quanh contour
        x, y, w, h = cv2.boundingRect(contour)
        if y > 0:
            rectangles.append((x, y+y_them, w, h))
    rectangles = sorted(rectangles, key=lambda rect: rect[2] * rect[3], reverse=True)

    return rectangles  
import win32api
MOUSEEVENTF_MOVE = 0x0001          # mouse move
MOUSEEVENTF_LEFTDOWN = 0x0002      # left button down
MOUSEEVENTF_LEFTUP = 0x0004        # left button up
MOUSEEVENTF_ABSOLUTE = 0x8000  
import ctypes
from ctypes import wintypes

EnumChildWindows = ctypes.windll.user32.EnumChildWindows
EnumChildProc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, ctypes.POINTER(ctypes.c_int))
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
GetWindowText = ctypes.windll.user32.GetWindowTextW
user32 = ctypes.WinDLL('user32', use_last_error=True)

def click(x, y):
    # Set the cursor position
    ctypes.windll.user32.SetCursorPos(x, y)
    
    # Simulate mouse left button down
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.05)  # Add a small delay to simulate the click
    # Simulate mouse left button up
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
def enum_child_windows_proc(hwnd, lParam):
    # Thêm các HWND của cửa sổ con vào danh sách
    handles_list.append(hwnd)
    return True  # tiếp tục liệt kê

# Hàm lấy tất cả các handle của cửa sổ con
def get_child_handles(parent_handle):
    global handles_list
    handles_list = []

    # Tạo một con trỏ cho lParam (trong Python, có thể dùng None hoặc ctypes.byref)
    EnumChildWindows(parent_handle, EnumChildProc(enum_child_windows_proc), None)

    return handles_list
GetClassName = ctypes.windll.user32.GetClassNameW
def find_child_handle(parent_handle, class_name):
    check =False
    child_handles = get_child_handles(parent_handle)
    for hwnd in child_handles:
        length = GetWindowTextLength(hwnd)
        class_name = ctypes.create_unicode_buffer(256)  # Bộ đệm để chứa tên lớp
        GetClassName(hwnd, class_name, 256)  
        buff = ctypes.create_unicode_buffer(length + 1)
        GetWindowText(hwnd, buff, length + 1)
        if "moon-bix" in str(buff.value):
            check=True
        #print(hwnd,buff.value,class_name.value)
        
        if "Chrome_RenderWidgetHostHWND" in str(class_name.value):
            return child_handles[2],child_handles[3],check
    
    return 0,0,check
def click111(hWnd,x, y):

    lParam = win32api.MAKELONG(x, y)
    win32gui.SendMessage(hWnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    win32gui.SendMessage(hWnd, win32con.WM_LBUTTONUP, None, lParam)
def get_telegram_windowstele():
    telegram_windows = []

    def enum_window_callback(hWnd, lParam):
        if win32gui.IsWindowVisible(hWnd):
            class_name = win32gui.GetClassName(hWnd)
            if "Qt51" in class_name:  # # Kiểm tra class name của Telegram
                window_text = win32gui.GetWindowText(hWnd)
                if "Telegram" in window_text:
                    set_window_size(hWnd, 350, 550) 
                    # Lấy tọa độ của khung ứng dụng
                    left, top, right, bottom = win32gui.GetWindowRect(hWnd)
                  
                    width = right - left
                    height = bottom - top
                    telegram_windows.append((hWnd, window_text, (left, top, width, height)))

    # Gọi EnumWindows với callback
    win32gui.EnumWindows(enum_window_callback, None)
    
    return telegram_windows

def gettele():
    telegram_windows1=[]
    telegram_windows = get_telegram_windowstele()
    for hwnd, title, (left, top, width, height) in telegram_windows:
        child_handles,child_handles1,check=find_child_handle(hwnd, "Chrome Legacy Window")
        if check:
            telegram_windows1.append((hwnd,child_handles,child_handles1,title, (left, top, width, height)))
        
    return telegram_windows1
def extend_line_to_edges(point1, point2, image_size):
    height, width = image_size
    x1, y1 = point1
    x2, y2 = point2

    # Tính toán hệ số góc (slope) và hệ số cắt (intercept)
    if x2 - x1 == 0:  # Đường thẳng thẳng đứng
        return (x1, 0), (x1, height)
    
    slope = (y2 - y1) / (x2 - x1)
    
    # Tính điểm giao với cạnh trên và dưới của hình ảnh
    x_top = int((0 - y1 + slope * x1) / slope)
    x_bottom = int((height - y1 + slope * x1) / slope)

    # Tính điểm giao với cạnh trái và phải của hình ảnh
    y_left = int(slope * (0 - x1) + y1)
    y_right = int(slope * (width - x1) + y1)

    # Tìm tọa độ hợp lệ trong các cạnh của hình ảnh
    extended_points = []
    if 0 <= x_top < width:
        extended_points.append((x_top, 0))
    if 0 <= x_bottom < width:
        extended_points.append((x_bottom, height))
    if 0 <= y_left < height:
        extended_points.append((0, y_left))
    if 0 <= y_right < height:
        extended_points.append((width, y_right))

    # Trả về điểm đầu tiên và điểm cuối cùng để vẽ
    if len(extended_points) >= 2:
        return extended_points[0], extended_points[1]
def does_line_intersect_box(point1, point2, box):
    x, y, w, h = box
    # Các điểm của hình chữ nhật
    box_points = [
        (x, y),  # Top-left
        (x + w, y),  # Top-right
        (x, y + h),  # Bottom-left
        (x + w, y + h)  # Bottom-right
    ]
    
    start = (x,y+h//2)
    end= (x+w,y+h//2)
    # if do_lines_intersect(point1, point2, start, end):
    #     return True
    # return False
    # Kiểm tra các cạnh của hình chữ nhật
    for i in range(4):
        start = box_points[i]
        end = box_points[(i + 1) % 4]
        if do_lines_intersect(point1, point2, start, end):
            return True
    return False
    


# Sử dụng hàm và in ra kết quả


    return rectangles  
def do_lines_intersect(p1, p2, p3, p4):
    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0  # Collinear
        return 1 if val > 0 else 2  # Clockwise or counterclockwise

    o1 = orientation(p1, p2, p3)
    o2 = orientation(p1, p2, p4)
    o3 = orientation(p3, p4, p1)
    o4 = orientation(p3, p4, p2)

    # Các trường hợp chung
    if o1 != o2 and o3 != o4:
        return True

    return False
def findcenter(frame,roi_image4):
    h1, w1, _ = roi_image4.shape
    frame=frame[:230,]
    result1 = cv2.matchTemplate(frame, roi_image4, cv2.TM_CCOEFF_NORMED)
    loc2= cv2.minMaxLoc(result1)
    center1=(0,0)
    check=False
    if loc2[1] >= 0.85:
        top_left = loc2[3]
        bottom_right = (top_left[0] + w1, top_left[1] + h1)
        center1 = (int((top_left[0] + bottom_right[0]) / 2+3), int(top_left[1] + h1)-5)
        check=True
    return center1,check
def findcenter123(frame,roi_image4):
    
    h1, w1, _ = roi_image4.shape
    result1 = cv2.matchTemplate(frame, roi_image4, cv2.TM_CCOEFF_NORMED)
    loc2= cv2.minMaxLoc(result1)
    center1=(0,0)
    check=False
    if loc2[1] >= 0.85:
        top_left = loc2[3]
        bottom_right = (top_left[0] + w1, top_left[1] + h1)
        center1 = (int((top_left[0] + bottom_right[0]) / 2), int(top_left[1] + h1)-5)
        check=True
    return center1,check
def findcenterName(frame,roi_image4):
    h1, w1, _ = roi_image4.shape
  
    result1 = cv2.matchTemplate(frame, roi_image4, cv2.TM_CCOEFF_NORMED)
    loc2= cv2.minMaxLoc(result1)
    center1=(0,0)
    check=False
    
    if loc2[1] >= 0.75:
        top_left = loc2[3]
        bottom_right = (top_left[0] + w1, top_left[1] + h1)
        center1 = (int((top_left[0] + bottom_right[0]) / 2+3), int(top_left[1] + h1)-5)
        check=True
    
       
    return center1,check
