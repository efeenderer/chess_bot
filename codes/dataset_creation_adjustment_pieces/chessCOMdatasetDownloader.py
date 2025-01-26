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

BASE_URL = "https://images.chesscomfiles.com/chess-themes/pieces"

piece_types = ['neo','game_room','wood','glass','gothic','classic','metal','bases','neo_wood','icy_sea','club','ocean','newspaper','space','cases','condal','8_bit',
               'marble','book','alpha','bubblegum','dash','graffiti','light','lolz','luca','maya','modern','nature','neon','sky','tigers','tournament','vintage']

piece_names = ['bp','wp',
               'bn','wn',
               'bb','wb',
               'br','wr',
               'bq','wq',
               'bk','wk']

sizes = np.linspace(100,300,9)

flag = False

for piece_type in piece_types:
    for piece_name in piece_names:
        for size in sizes:
            
            if not flag and piece_type == 'metal' and piece_name == 'wn' and int(size) == 300:
                flag = True

            if flag:
                URL = BASE_URL+"/"+piece_type+"/"+str(int(size))+"/"+piece_name+".png" #https://images.chesscomfiles.com/chess-themes/pieces/tournament/101/wq.png
                try:
                    response = requests.get(URL,headers=headers)
                    response.raise_for_status()

                    directory = r"DOWNLOAD_LOCATION" ##########################################################

                    filename = os.path.join(directory+"\\"+URL.split("/")[-3]+"_"+URL.split("/")[-2]+"_"+URL.split("/")[-1])

                    with open(filename, 'wb') as f:
                        f.write(response.content)
                        f.close()

                    print(f"İndirildi: {filename}")
                    t.sleep(0.1)
                    
                except requests.RequestException as e:
                    print(f"İndirmede hata oluştu: {URL} - {e}") 



            





