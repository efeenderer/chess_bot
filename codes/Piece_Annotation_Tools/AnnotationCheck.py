import cv2
import os
import numpy as np

def getFilePath():
    file_path = os.path.dirname(__file__)

    return file_path[0].upper() + file_path[1:]

def UpperPath(path):
    upper_path = os.path.dirname(path)

    return upper_path[0].upper() + upper_path[1:]

__path__ = getFilePath() #Directory of the current file

def draw_box(img, box, color=(0,255,0)):
    h, w = img.shape[:2]
    x1, y1 = int((box[0] - box[2]/2) * w), int((box[1] - box[3]/2) * h)
    x2, y2 = int((box[0] + box[2]/2) * w), int((box[1] + box[3]/2) * h)
    cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

image_folder = r'TEST_IMAGES_WILL_BE_PUT_HERE'

label_folder = r'LABELS_OF_TEST_IMAGES_WILL_BE_PUT_HERE'

for filename in os.listdir(image_folder):
    if filename.endswith(('.jpg', '.png', '.jpeg')):
        image_path = os.path.join(image_folder, filename)
        label_path = os.path.join(label_folder, os.path.splitext(filename)[0] + '.txt')
        
        if os.path.exists(label_path):
            img = cv2.imread(image_path)
            
            with open(label_path, 'r') as f:
                lines = f.readlines()
            
            for line in lines:
                data = list(map(float, line.strip().split()))
                draw_box(img, data[1:])
            
            cv2.imshow('Image with Annotations', img)
            key = cv2.waitKey(0)
            
            if key == ord('q'):
                break

cv2.destroyAllWindows()
