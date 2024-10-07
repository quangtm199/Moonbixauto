import win32gui
import pyautogui
import time
import numpy as np
import cv2
import win32api
import win32con
import random     
from PIL import Image
from multiprocessing import Queue
from multiprocessing import Process
import multiprocessing 
from utils import gettele,click,findcenter123,findmap,does_line_intersect_box,click111
import ctypes
# Define constants for mouse events
MOUSEEVENTF_MOVE = 0x0001          # mouse move
MOUSEEVENTF_LEFTDOWN = 0x0002      # left button down
MOUSEEVENTF_LEFTUP = 0x0004        # left button up
MOUSEEVENTF_ABSOLUTE = 0x8000      # absolute move

# Define the mouse_event function from user32.dll
user32 = ctypes.WinDLL('user32', use_last_error=True)
tstart=time.time()
TrackerPerson =  dict() 
roi_image14=cv2.imread(r"resource/25.png")

start=0    
starty=0


       
def CommitSQL(TrackerPerson):
    time.sleep(1)
    while True :
        try:
            screenshot = pyautogui.screenshot()
        except:
           
            continue
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        h,w,_=frame.shape
        for i in telegram_windows1:
            hwnd,child_handles,child_handles1, title, (left, top, width, height) = i
            frame1 =frame[max(top,0):min(top + height,h),max(left,0):min(left + width ,w)]
           
            if TrackerPerson[hwnd].qsize()>10:
                TrackerPerson[hwnd].get()
                continue
            TrackerPerson[hwnd].put((frame1.copy(),left,top,width,height))

        time.sleep(0.03)
        
def getRUn(TrackerPerson,hwnd,child_handles1):
   
    
    loaded_array = np.load(r'resource/listtoadovalue6.npy')
    loaded_arrayImage = np.load(r'resource/listtoadoImage6.npy')    
   # D:\MMO\Tool-20240615T090125Z-001\Tool\Ceoio\listtoadovalue5.npy
  
    while True:
        
        if TrackerPerson.qsize()!=0:
            frame,left,top,width,height = TrackerPerson.get()
          
            tstart = time.time()
            
            while True:
                frame,left,top,width,height  = TrackerPerson.get()
                try:
                    center1, check123 = findcenter123(frame, roi_image14)
                except:
                
                    None
                if check123==True:
                    break
            open_cv_image=frame
            maplocation = findmap(open_cv_image[200:], 200)
            checkclick=False
            while True:
                if time.time() - tstart > 50:
                    frame,left,top,width,height  = TrackerPerson.get()
                    center1, check123 = findcenter123(frame, roi_image14)
                
                    if check123==False:
                        break
                    
                if checkclick:
                    for i in range(30):
                        frame2,left,top,width,height = TrackerPerson.get()
                    
                if checkclick:
                    maplocation = findmap(frame2[200:], 200)
                checkclick=False
                frame2,left,top,width,height = TrackerPerson.get()
                open_cv_image =frame2
                value = open_cv_image[147:175,125:225]
                check = False
                minvalue = 800
                value123=0
                for i in range(0, loaded_arrayImage.shape[0], 1):
                    item = loaded_arrayImage[i]
                    try:
                        difference = cv2.subtract(item, value)
                    except:
                        print(item.shape,value.shape)
                    gray_difference = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
                    _, thresh_diff = cv2.threshold(gray_difference, 40, 255, cv2.THRESH_BINARY)
                    different_pixels = cv2.countNonZero(thresh_diff)

                    if different_pixels < minvalue:
                        minvalue = different_pixels
                        value123 = i

                    if minvalue < 100:
                        check = True
                        break
                
                if minvalue > 100:
                    None
                else:
                    extended_point1, extended_point2 = loaded_array[value123]
                    #extended_point1, extended_point2 = extend_line_to_edges(center, center1, frame2.shape[:2])
                    
                    for box in maplocation:
                        x1, y1, w1, h1 = box
                        if does_line_intersect_box(extended_point1, extended_point2, box):
                            try:
                                random_int = random.randint(-10, 10)
                             
                                click111(hwnd,100+random_int,   240+random_int)
                                click111(child_handles1,100+random_int,   240+random_int)
                                checkclick=True
                                
                                # cv2.rectangle(frame2, (x1, y1), (x1 + w1, y1 + h1), (255, 0, 0), 2)
                               
                            except:
                                break
                            break
                # cv2.line(frame2, extended_point1, extended_point2, (0, 255, 0), 2)           
                # cv2.imshow(str(hwnd),frame2)
                # cv2.waitKey(1)
                                


telegram_windows1= gettele()
#print(telegram_windows1)
# Khởi tạo thread cho mỗi cửa sổ
if __name__ == "__main__":
    # Initialize processes for each window
    processes = []
    truid=0
    CHECKALL=True
    for i in range(len(telegram_windows1)):
        hwnd,child_handles,child_handles1, title, (left, top, width, height) = telegram_windows1[i]
        TrackerPerson[hwnd]=Queue()
        idx=i
        if i <6:
            start=start+width
        if i==6:
            idx=i-6
            start=0
            starty=height-20
        
        if i >6:
            start=start+width
            idx=i-6
        if i==0:
            start=0
        if CHECKALL:
            if hwnd:
                win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, start-truid*idx, starty, 0, 0, win32con.SWP_NOSIZE)
                time.sleep(0.1)
                if CHECKALL:
                    click(left+50,top+150)
                    time.sleep(0.3)
                    pyautogui.press('f5')
                    time.sleep(0.3)
    telegram_windows=[] 
    for i in range(len(telegram_windows1)):
        hwnd,child_handles,child_handles1, title, (left, top, width, height) = telegram_windows1[i]
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        if CHECKALL:
            time.sleep(0.3)
            click(left+50,top+150)
            pyautogui.press('f12')
        telegram_windows.append([hwnd,child_handles,child_handles1, title, (left, top, width, height)])

    telegram_windows1=telegram_windows     
    for i in range(len(telegram_windows1)):
        hwnd,child_handles,child_handles1, title, (left, top, width, height) = telegram_windows1[i]
     
        proc6 = Process(target=getRUn,args=(TrackerPerson[hwnd],child_handles,child_handles1))
        time.sleep(1)
        proc6.daemon=True

        proc6.start()

    proc5 = Process(target=CommitSQL,args=(TrackerPerson,))
    proc5.daemon=True
    proc5.start()
 
    proc5.join()
    proc6.join()
    #cv2.destroyAllWindows()
    
    # for i in range(len(telegram_windows1)):
    #     hwnd, title, (left, top, width, height) = telegram_windows1[i]
    #     process = multiprocessing.Process(target=process_window, args=(hwnd, title, left, top, width, height))
    #     processes.append(process)
    #     process.start()

    # Wait for all processes to complete
    # for process in processes:
    #     process.join()
