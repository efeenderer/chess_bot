import cv2 as cv
import os
import numpy as np
import random

def getFilePath():
    file_path = os.path.dirname(__file__)

    return file_path[0].upper() + file_path[1:]

def UpperPath(path): #Upper folder of the argument "path"
    upper_path = os.path.dirname(path)

    return upper_path[0].upper() + upper_path[1:]

__path__ = getFilePath()    #Directory of the current file


path = r"IMAGES_THAT_WILL_BE_RESIZED" ###########################################
new_path =r"NEW_LOCATION_FOR_RESIZED_IMAGES" ###########################################


for file in os.listdir(new_path):
    try:
        os.remove(new_path+"\\"+file)
    except: pass

i=0
for file in os.listdir(path):
    i=i+1
    image = cv.imread(path+"\\"+file)
    size = random.randint(30,108)*10
    resized_image = cv.resize(image, (size,size),interpolation=cv.INTER_LINEAR)
    kernel = np.array([[-1, -1, -1],[-1,9,-1],[-1,-1,-1]])
    sharpened_image = cv.filter2D(resized_image,-1,kernel)

    choice = random.randint(0,1)

    if size < 460:
        choice = 1
    try:
        cv.imwrite(new_path+"\\"+file,sharpened_image if choice==0 else resized_image)
        print(f"File {file} has succesfully been resized. {i}/{len(os.listdir(path))}")
    except:
        print(f"File {file} couldn't have been resized. {i}/{len(os.listdir(path))}")