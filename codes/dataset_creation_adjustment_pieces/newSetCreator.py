import os
import shutil
import time as t
from PIL import Image
import random


def getFilePath():
    file_path = os.path.dirname(__file__)

    return file_path[0].upper() + file_path[1:]

def UpperPath(path): #Upper folder of the argument "path"
    upper_path = os.path.dirname(path)

    return upper_path[0].upper() + upper_path[1:]

__path__ = getFilePath()    #Directory of the current file


boards_path = os.path.join( UpperPath(UpperPath(__path__)) ,r"dataset\board_set\chess_com\all_boards_cropped" )

piece_types_path = os.path.join( UpperPath(UpperPath(__path__)) ,r"dataset\Dataset Chess Com by Type PNG\125" )

save_path = r"E:\Python_Projeler\ComputerVisionProjects\chess_bot\codes\dataset_creation_adjustment_pieces\CreationTests\test_results"

def getRandomType():
    piece_types = os.listdir(piece_types_path)
    return random.choice(piece_types)

def getRandomPiece(type):

    path = piece_types_path+"\\"+type

    pieces = os.listdir(path)

    return random.choice(pieces)

if __name__ == "__main__":


    for board in os.listdir(boards_path):
        for i in range(5):
            board_image_path = boards_path + "\\" + board
            board_name = board.split(".")[-2]
            board_img = Image.open(board_image_path).convert('RGB')
            x_size = board_img.getbbox()[2]
            y_size = board_img.getbbox()[3]

            type = getRandomType()
            pieces = []
            piece_centers = set()

            piece_path = piece_types_path + "\\" + type

            for piece_amount in range(random.randint(0,40)):
                piece_x_center = int((x_size / 16) * (2*random.randint(0,7)+1))-54
                piece_y_center = int((y_size / 16) * (2*random.randint(0,7)+1))-50

                piece_centers.add((piece_x_center,piece_y_center))
                
                pieces.append(getRandomPiece(type))        
            #print(f"{len(pieces)} - {len(piece_centers)} ")            

            for index,coordinates in enumerate(piece_centers):
                piece_img = Image.open(piece_path + "\\" + pieces[index]).convert('RGBA')
                new_width = int(piece_img.width * 0.85)  # Genişliği %80'e düşür
                new_height = new_width  # Yüksekliği %85'e düşür
                if hasattr(Image, 'Resampling'):
                    resample_method = Image.Resampling.LANCZOS
                else:
                    resample_method = Image.ANTIALIAS

                piece_img = piece_img.resize((new_width, new_height), resample_method)


                piece_img.copy()
                board_img.paste(piece_img,coordinates,piece_img)
            
            save_file_path = os.path.join(save_path,board_name+f"_{i}"+".jpg")
            print(piece_centers)
            try:
                board_img.save(save_file_path)
                #print(f"{board} kaydedildi, konum: {save_file_path}")
            except Exception as e:
                print(f"{board} kaydedilemedi. Hata: {e}")
            



        











