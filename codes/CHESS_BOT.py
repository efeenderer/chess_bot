import os
import mss
from ultralytics import YOLO
import cv2 as cv
import numpy as np
from PIL import Image
from stockfish import Stockfish
import time as t
from queue import Queue
import threading


try:
        sct = mss.mss()
except Exception as e:
    print(f"There was an error creating sct. Error: {e}")

def getFilePath():
    file_path = os.path.dirname(__file__)

    return file_path[0].upper() + file_path[1:]
def UpperPath(path):
    upper_path = os.path.dirname(path)

    return upper_path[0].upper() + upper_path[1:]

__path__ = getFilePath()


piece_by_id = {0:'p',6:'P',
               1:'n',7:'N',
               2:'b',8:'B',
               3:'r',9:'R',
               4:'q',10:'Q',
               5:'k',11:'K'}

piece_map = [] 
#Piece Map will look like this:
#[[p,p,p,p,p,0,0,0],
# [b,B,0,0,0,0,0,0],
# .................
# .................
# .................
# ......,K,Q,0,0,R]]

def Screenshot():
    return sct.shot()

def DetectBoard():
    try:
        frame = np.array(Screenshot())
        frame = cv.cvtColor(frame,cv.COLOR_RGB2BGR)
        N = 1200
        frame = cv.resize(frame,(N,int(N/1.777)))   # N x N/1.777 --- 16:9
                        
        results = board_model(frame)

        boxes = results[0].boxes
        
        if len(boxes) > 0:
            box = boxes[0].xyxy[0]
            x1,y1,x2,y2 = map(int,box)
            board = frame[y1:y2,x1:x2]
            return board
        return None
    except Exception as e:
        print(f"Error in detect_board: {e}")
        return None

def DetectPieces(board):
    if board == None:
        return
    board = cv.cvtColor(board,cv.COLOR_RGB2BGR)

    

def ProcessImage():
    process_time = 1 #For optimization purposes. If the elapsed time does not exceed this value, the program will remain constant. 
    last_time = t.time()
    base_time = last_time

    while True: #Processing loop
        current_time = t.time()
        try:
            if process_time >= current_time - last_time:    #Cooldown part. Here, there won't be any process. Maybe some tests or print like functions.
                #print(f"Waiting... Elapsed time for this turn: {current_time - last_time:.2f}s") 
                print(f"Total elapsed time: {current_time - base_time:.2f}s")
                
            else:
                last_time = current_time
                board = DetectBoard()
                DetectPieces(board)

        except Exception as e:
            print(f"There was an error taking screenshot. Error: {e}")
        t.sleep(0.2)


def FindFEN():
    pass

def MainLoop():
    
    
    while True: #main loop
        try:
            print(f"I feel good....nana nana nana na")
            t.sleep(1)
        except Exception as e:
            print(f"An Error occured, Error:{e}")


if __name__ == "__main__":
    board_model = YOLO(os.path.join(__path__,'models\\board_model.pt'))
    piece_model = YOLO(os.path.join(__path__,'models\\piece_model.pt'))

    image_processing_thread = threading.Thread(target=ProcessImage,daemon=True)
    main_thread = threading.Thread(target=MainLoop,daemon=True)

    image_processing_thread.start()
    main_thread.start()

    image_processing_thread.join()
    main_thread.join()



