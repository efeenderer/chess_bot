from ultralytics import YOLO
import multiprocessing
import numpy as np
import pyautogui
import cv2
import os

def getFilePath():
    file_path = os.path.dirname(__file__)

    return file_path[0].upper() + file_path[1:]

def UpperPath(path):
    upper_path = os.path.dirname(path)

    return upper_path[0].upper() + upper_path[1:]

__path__ = getFilePath()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    model = YOLO("yolo11n.yaml")
    data_path = os.path.join(__path__, 'pieces.yaml')
    results = model.train(data=data_path,epochs=150,batch=-1)

