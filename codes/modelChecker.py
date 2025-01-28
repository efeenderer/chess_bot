import threading
import queue
import cv2
import numpy as np
import time as t
from ultralytics import YOLO
import mss
import os
import torch 


image_queue = queue.Queue(maxsize=1)



def getFilePath():
    file_path = os.path.dirname(__file__)

    return file_path[0].upper() + file_path[1:]

def UpperPath(path):
    upper_path = os.path.dirname(path)

    return upper_path[0].upper() + upper_path[1:]

__path__ = getFilePath()

if __name__ == "__main__":
    if torch.cuda.is_available():
        board_model = YOLO(r"E:\Python_Projeler\runs\detect\train16\weights\best.pt").to('cuda')
        piece_model = YOLO(r"E:\Python_Projeler\runs\detect\train15\weights\best.pt").to('cuda')
    else:
        board_model = YOLO(r"E:\Python_Projeler\runs\detect\train16\weights\best.pt")
        piece_model = YOLO(r"E:\Python_Projeler\runs\detect\train15\weights\best.pt")

def detect_board(sct,monitor):
    try:
        screenshot = np.array(sct.grab(monitor))
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame = cv2.resize(frame, (1184, 666))

        results = board_model(frame)

        boxes = results[0].boxes
        
        if len(boxes) > 0:
            box = boxes[0].xyxy[0]
            x1,y1,x2,y2 = map(int,box)
            board = frame[y1:y2,x1:x2]
            return board
    except Exception as e:
        print(f"Error in detect_board: {e}")
        return None

def detect_pieces(frame):
    if frame is None:
        return cv2.imread(os.path.join(__path__, "face.jpg"))
    
    results = piece_model(frame,conf=0.8)
    result_image = results[0].plot(font_size=5)
    return cv2.cvtColor(result_image, cv2.COLOR_RGB2BGR)

def processImage():
    sct = mss.mss()
    monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}


    last_board_frame = None
    process_interval = 0.5  
    last_process_time = 0

    while True:
        current_time = t.time()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if current_time - last_process_time >= process_interval:
            try:
                board_frame = detect_board(sct, monitor)
                if board_frame is not None and not np.array_equal(board_frame, last_board_frame):
                    pieces = detect_pieces(board_frame)
                    last_board_frame = board_frame
                elif not image_queue.full():
                    image_queue.put(pieces)
                else:
                    image_queue.get()
                    image_queue.put(pieces)

            except Exception as e:
                print(f"Error in main loop: {e}")
            last_process_time = current_time
        t.sleep(0.1)

def display_window():
    cv2.namedWindow("Chess_bot", cv2.WINDOW_NORMAL)
    blank_image = np.zeros((480, 640, 3), np.uint8)
    
    last_frame = blank_image
    while True:
        if not image_queue.empty():
            last_frame = image_queue.get()
        frame = last_frame
        cv2.imshow("Chess_bot", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cv2.destroyAllWindows()



processing_thread = threading.Thread(target=processImage)
processing_thread.daemon=True
processing_thread.start()

display_thread = threading.Thread(target=display_window)
display_thread.daemon = True
display_thread.start()


try:
    while True:
        t.sleep(0.05)
except KeyboardInterrupt:
    print("Program sonlandiriliyor...")

# Temizlik işlemleri
cv2.destroyAllWindows()
del piece_model
del board_model

