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

def TakeScreenshot(sct):
    return sct.shot()

def DetectBoard():
    return None

def DetectPieces():
    pass

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
                print(f"Total elapsed time: {current_time - base_time:.2f}s")
                last_time = current_time


        except Exception as e:
            print(f"There was an error taking screenshot. Error: {e}")
        t.sleep(0.2)


def FindFEN(piece_map:list, ):
    pass

def MainLoop():
    try:
        sct = mss.mss()
    except Exception as e:
        print(f"There was an error creating sct. Error: {e}")
    
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



