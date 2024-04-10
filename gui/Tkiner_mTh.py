import tkinter
import cv2
from PIL import Image, ImageTk
import threading
import os
import sys
# 현재 스크립트가 있는 폴더의 경로를 뜯기 후 일시적으로 자동추가 하게함 건들지 말것
current_directory = os.path.dirname(os.path.abspath(__file__))
print(current_directory)
sys.path.append(current_directory)
os.environ['PYTHONPATH'] = current_directory + os.pathsep + os.environ.get('PYTHONPATH', '')

from  utills.utill import *


window = tkinter.Tk()
window.title("Camera with Threading")
window.geometry("880x480")
set_window(window)  # window 객체 설정

frame1=tkinter.Frame(window, relief="solid", bd=2)
frame1.pack(side="left", fill="both", expand=True)

frame2=tkinter.Frame(window, relief="solid", bd=2)
frame2.pack(side="right", fill="both", expand=True)
menu_builder = MenuBuilder(window)
menu_builder.add_menu("상위 메뉴 1", [
    {"label": "하위 메뉴 1-1"},
    {"label": "하위 메뉴 1-2"},
    {"separator": True},
    {"label": "종료", "command": close}
])

#canvas = tkinter.Canvas(frame1, width=640, height=480)
#canvas.pack()
#장치열기
cap = cv2.VideoCapture(0)
label= tkinter.Label(frame1)
label.pack(side="top")
#메인쓰레드에서 분기
threading.Thread(target=capture_video,args=(cap,label)).start()
#canvas.after(100, lambda: process_queue(canvas))

process_queue()
stop_button = tkinter.Button(frame2, text="Stop", command=stop_capture)
stop_button.pack(side=tkinter.RIGHT)

#button = tkinter.Button(frame2, text="이진화 처리", command=toggle_binary_mode)
#button.pack(side="bottom", expand=True, fill='both')

menu_builder.config_menu(window)

window.mainloop()
stop_capture()
cap.release()