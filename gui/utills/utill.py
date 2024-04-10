import cv2
import tkinter
from PIL import Image, ImageTk
import threading
import time
stop_thread = False
import queue
callback_queue = queue.Queue()
window = None  # 전역 변수로 선언
imgtk=None
def set_window(win):
    global window
    window = win
    
#def process_queue(canvas):
#    try:
#        while not callback_queue.empty():
#            callback = callback_queue.get_nowait()
#            callback()
#    except queue.Empty:
#        pass
#    canvas.after(1, lambda: process_queue(canvas))  # 10ms 후에 다시 큐 처리
    
#쓰레드열어서 구동
def process_queue():
    global callback_queue
    try:
        while True:
            # 큐에서 콜백 함수를 가져와 실행
            callback = callback_queue.get_nowait()
            callback()
            #imgtk_reference = callback.p
    except queue.Empty:
        # 큐가 비어 있으면 더 이상 처리할 작업이 없음
        pass
    window.after(1, process_queue)  # 10ms 후에 다시 큐 처리


#(Cap,label)
#def capture_video(cap,canvas):
#    global stop_thread,callback_queue,imgtk
#    while not stop_thread:
#        ret, frame = cap.read()
#        if ret:
#            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#            img = Image.fromarray(frame)
#            imgtk = ImageTk.PhotoImage(image=img)
#            #label.imgtk = imgtk  # 참조를 유지합니다.
#            #label.configure(image=imgtk)
#            callback = lambda img=imgtk: canvas.create_image(0, 0, anchor="nw", image=img)
#            #callback = lambda l=label, p=imgtk: l.configure(image=p)
#            callback_queue.put(callback)
# 

def capture_video(cap,label):
    global stop_thread,callback_queue,imgtk_reference 
    while not stop_thread:
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            label.imgtk = imgtk  # 참조를 유지합니다.
            imgtk_reference = imgtk
            #label.configure(image=imgtk)
            callback = lambda l=label : l.configure(image=imgtk_reference)
            callback_queue.put(callback)


def stop_capture():
    global stop_thread
    stop_thread = True
    
    
def toggle_binary_mode():
    global binary_mode
    # 이진화 모드 플래그를 토글
    binary_mode = not binary_mode

def close():
    window.quit()
    window.destroy()
    
class MenuBuilder:
    def __init__(self, window):
        self.menubar = tkinter.Menu(window)

    def add_menu(self, label, menu_items, is_radiobutton=False, is_checkbutton=False):
        menu = tkinter.Menu(self.menubar, tearoff=0)
        for item in menu_items:
            if is_radiobutton:
                menu.add_radiobutton(label=item.get("label"), state=item.get("state", "normal"))
            elif is_checkbutton:
                menu.add_checkbutton(label=item.get("label"))
            else:
                menu.add_command(label=item.get("label"), command=item.get("command", None))
                if "separator" in item:
                    menu.add_separator()
        self.menubar.add_cascade(label=label, menu=menu)
        return menu

    def config_menu(self, window):
        window.config(menu=self.menubar)
        
        
def process_image_async(image, callback):
    # 이미지 처리 작업을 비동기적으로 실행
    # 예를 들어, 얼굴 감지 등의 이미지 처리 작업 수행
    processed_image = image  # 간단한 예시로 원본 이미지를 그대로 사용
    
    # 처리가 완료되면 콜백 함수 호출
    callback(processed_image)

def update_ui(image):
    # UI 업데이트를 위한 콜백 함수
    # 이미지를 tkinter Label에 표시
    imgtk = ImageTk.PhotoImage(image=Image.fromarray(image))
    label.imgtk = imgtk
    label.configure(image=imgtk)

def capture_and_process_video(cap, label):
    while True:
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # 이미지 처리 함수를 비동기적으로 실행
            threading.Thread(target=process_image_async, args=(frame, update_ui)).start()
