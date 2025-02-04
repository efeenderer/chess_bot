import os
import mss
from ultralytics import YOLO
import cv2 as cv
import numpy as np
from PIL import Image
from stockfish import Stockfish
import time as t
from screeninfo import get_monitors


monitor = {"top": 0, "left": 0, "width": int(get_monitors()[0].width), "height": int(get_monitors()[0].height)}
sct = mss.mss()

"""try:
        sct = mss.mss()
except Exception as e:
    print(f"There was an error creating sct. Error: {e}")"""

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
# ......,K,Q,0,0,R]] Obiviously, they're all gonna be chars




"""
def Screenshot():
    with mss.mss() as sct:          #I kept getting this error: AttributeError: '_thread._local' object has no attribute 'srcdc'. Don't know why but getting screenshots this way solved that problem. 
        return sct.grab(monitor)    #I'll work on that later to see what was the problem
    """


def DetectBoard():
    try:
        #screenshot = np.array(sct.grab(monitor))
        screenshot = np.array(sct.grab(monitor))
        frame = np.array(screenshot)
        frame = cv.cvtColor(screenshot,cv.COLOR_RGB2BGR)
        #frame = cv.resize( frame , ( 1184 , 666 ) )                TI
                        
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

def DetectPieces(board):
    if board is None:
        return np.zeros((480, 640, 3), np.uint8)
    
    #board = cv.cvtColor(board, cv.COLOR_RGB2BGR) 

    results = piece_model(board,conf=0.8)

    image = results[0].plot(font_size=15)

    return cv.cvtColor(image,cv.COLOR_RGB2BGR)


def FindFEN():
    pass

def MainLoop():

    cv.namedWindow("lala",cv.WINDOW_NORMAL)

    while True: #main loop
        try:
            #print(f"I feel good....nana nana nana na")
            board_crop = DetectBoard()
            image_pieces = np.zeros((500,500,3), np.uint8)
            if board_crop is not None:
                image_pieces = DetectPieces(board_crop)
            
            cv.imshow("lala",image_pieces)

            if cv.waitKey(1) & 0xFF == ord('q'):
                break
            
        except Exception as e:
            print(f"An Error occured, Error:{e}")
        t.sleep(0.1)


if __name__ == "__main__":
    board_model = YOLO(os.path.join(__path__,'models\\board_model.pt')).to("cuda")
    piece_model = YOLO(r"E:\Python_Projeler\ComputerVisionProjects\chess_bot\codes\models\piece_model.pt").to("cuda")

    MainLoop()



