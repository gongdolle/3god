import tkinter as tk
from PIL import Image, ImageTk
import cv2
import threading
import queue
import time

class VideoCamera:
    def __init__(self):
        self.video_capture = cv2.VideoCapture(0)
        self.video_capture.set(cv2.CAP_PROP_FPS, 30)  # FPS 설정

    def __del__(self):
        self.video_capture.release()

    def read_image(self):
        ret, frame = self.video_capture.read()
        if ret:
            return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        else:
            return None

class AppGui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("multi")

        self.label = tk.Label(self.root)
        self.label.pack()

        self.camera = VideoCamera()
        self.callback_queue = queue.Queue()
        self.stop_thread = False

        self.update_ui()

    def update_ui(self):
        self.process_queue()
        
        if image is not None:
            processed_image = self.process_image_async()
            self.callback_queue.put(lambda p=processed_image: self.update_label(self.label, p))
        if not self.stop_thread:
            self.root.after(1, self.update_ui)

    def process_image_async(self):
        # 이미지 처리를 비동기화
        image = self.camera.read_image()
          # 이미지 처리 시뮬레이션을 위한 임의의 대기 지금은 비워둠
        return ImageTk.PhotoImage(image=Image.fromarray(image))

    def update_label(self, label, photo):
        label.configure(image=photo)
        label.image = photo  # 참조 유지

    def process_queue(self):
        while True:
            try:
                callback = self.callback_queue.get_nowait()
                callback()
            except queue.Empty:
                break

    def run(self):
        self.root.mainloop()

app_gui = AppGui()
app_gui.run()