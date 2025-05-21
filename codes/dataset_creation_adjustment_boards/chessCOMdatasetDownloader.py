import numpy as np
import time as t
import os
import requests

def getFilePath():
    file_path = os.path.dirname(__file__)

    return file_path[0].upper() + file_path[1:]

def UpperPath(path): #Upper folder of the argument "path"
    upper_path = os.path.dirname(path)

    return upper_path[0].upper() + upper_path[1:]

__path__ = getFilePath()    #Directory of the current file

headers = {'User-Agent': 'DatasetCollectionForSchoolProject/ (efe.ender.er@gmail.com)'} #I'm too afraid to have problems for trying to download this fkn set

BASE_URL = "https://images.chesscomfiles.com/chess-themes/boards_3d"

board_types = ['green','dark_wood','brown','icy_sea','newspaper','walnut','sky','lolz','stone','bases','8_bit','marble','purple','translucent','metal','tournament','dash',
               'burled_wood','blue','bubblegum','checkers','graffiti','light','neon','orange','overlay','parchment','red','sand','tan']

flag = False

for board_type in board_types:
    for i in range(10):

        URL = BASE_URL+"/"+"board_"+board_type+".jpg"     #https://images.chesscomfiles.com/chess-themes/boards_3d/board_wood.jpg
        try:
            response = requests.get(URL,headers=headers)
            response.raise_for_status()

            d = r"DOWNLOAD_LOCATION" ##########################################################
            
            file_path_string = d + "\\" + URL.split("/")[-1].split(".")[-2]+"_"+str(i)+".jpg"

            file_path = os.path.join(file_path_string)

            with open(file_path, 'wb') as f:
                f.write(response.content)
                f.close()

            print(f"Indirildi: {file_path}")
            t.sleep(0.1)
            
        except requests.RequestException as e:
            print(f"Indirmede hata oluştu: {URL} - {e}") 
