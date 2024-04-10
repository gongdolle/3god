import tkinter
import cv2
#PILImage와 ImageTk: PIL(Python Imaging Library)의 모듈, 이미지 작업을 위해 사용되며, 
from PIL import Image
from PIL import ImageTk
#ImageTk는 Tkinter와 함께 이미지를 처리하고 표시하는 데 사용됩니다
def update_frame():
    global cap,binary_mode
    ret, frame = cap.read()
    if ret:
       if binary_mode:
           #이진화
           frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
           _, frame = cv2.threshold(frame,100,255,cv2.THRESH_BINARY)
           frame= cv2.cvtColor(frame,cv2.COLOR_GRAY2RGB)
           img = Image.fromarray(frame)
           imgtk = ImageTk.PhotoImage(image=img)
           label.imgtk = imgtk
           label.configure(image=imgtk)
           print("실행됨")
       else:
           #아닐경우 
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        label.imgtk = imgtk
        label.configure(image=imgtk)
        
    window.after(10, update_frame)  # 10ms 후에 update_frame 함수를 다시 호출
    
def toggle_binary_mode():
    global binary_mode
    # 이진화 모드 플래그를 토글
    binary_mode = not binary_mode

def close():
    window.quit()
    window.destroy()

#flag
binary_mode = False
frame = None

window=tkinter.Tk()
window.title("3god")
window.geometry("880x480")

menubar=tkinter.Menu(window)
menu_1=tkinter.Menu(menubar, tearoff=0)
menu_1.add_command(label="하위 메뉴 1-1")
menu_1.add_command(label="하위 메뉴 1-2")
menu_1.add_separator()
menu_1.add_command(label="종료", command=close)
menubar.add_cascade(label="상위 메뉴 1", menu=menu_1)
window.config(menu=menubar)

frame1=tkinter.Frame(window, relief="solid", bd=2)
frame1.pack(side="left", fill="both", expand=True)

frame2=tkinter.Frame(window, relief="solid", bd=2)
frame2.pack(side="right", fill="both", expand=True)


cap=cv2.VideoCapture(0)
label= tkinter.Label(frame1)
label.pack(side="top")

button = tkinter.Button(frame2, text="이진화 처리", command=toggle_binary_mode)
button.pack(side="bottom", expand=True, fill='both')

update_frame()  # 카메라로부터 영상을 받아와서 업데이트하는 함수를 처음 호출

window.mainloop()
cap.release()  # 카메라 장치 해제