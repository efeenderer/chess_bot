from PIL import Image
import os
import shutil
import random



def getFilePath():
    file_path = os.path.dirname(__file__)

    return file_path[0].upper() + file_path[1:]

def UpperPath(path):
    upper_path = os.path.dirname(path)

    return upper_path[0].upper() + upper_path[1:]

__path__ = getFilePath()

boards_path = os.path.join( UpperPath(UpperPath(__path__)) ,r"dataset\board_set\chess_com\all_boards" ) #__path__+r"\Tests\boards"
backgrounds_path = os.path.join( UpperPath(UpperPath(__path__)) ,r"dataset\board_set\chess_com\backgrounds" ) #__path__+r"\Tests\background"
images_path = os.path.join( UpperPath(UpperPath(__path__)) ,r"dataset\board_set\chess_com\images" ) #__path__+r"\Tests\images"
labels_path = os.path.join( UpperPath(UpperPath(__path__)) ,r"dataset\board_set\chess_com\labels" ) #__path__+r"\Tests\labels"

print(backgrounds_path)

def Annotation(Topleft_x: int , Topleft_y: int, background_lengths: tuple,board_length: int, board_name: str, index):
    board_name_txt = board_name.split(".")[-2]+f"_{index}"+".txt"


    center_x = (Topleft_x + board_length/2)/background_lengths[0]
    center_y = (Topleft_y + board_length/2)/background_lengths[1]
    length_x = board_length/background_lengths[0]
    length_y = board_length/background_lengths[1]
    try:
        annotation_path = os.path.join(labels_path,board_name_txt)
        if not os.path.exists(annotation_path):
            os.path.join(labels_path,board_name_txt)

        with open(annotation_path,"w+") as f:
            TEXT = "0 "+f"{center_x} {center_y} {length_x} {length_y}"
            f.write(TEXT)
    except Exception as e:
        print(f"Annotation dosyasi olusturulamadi. HATA: {e}")

def PutBoardToBackground(board_img: Image.Image,board_name ,background: Image.Image, index:int):

    board_img = board_img.convert('RGB')
    background = background.convert('RGB')

    background_width = background.size[0]
    background_height = background.size[1]

    board_length = board_img.size[0]

    min_side = min(background_height,background_width)

    if min_side <= board_length:
        random_size = random.randint(int(min_side/5),min_side-25)
        board_img = board_img.resize((random_size,random_size))
    
   
    board_length = board_img.size[0]

    Topleft_x = random.randint(0,background_width-1-board_length)
    Topleft_y = random.randint(0,background_height-1-board_length)

    paste_xy = (Topleft_x,Topleft_y)

    board_img.copy()

    background.paste(board_img,paste_xy)

    name = board_name.split(".")[-2]+f"_{index}"+"."+board_name.split(".")[-1]
    print(name)
    try:
        background.save(os.path.join(images_path,name))
    except Exception as e:
        print(e)
    Annotation(Topleft_x, Topleft_y, (background_width,background_height) ,board_length ,board_name,index=index)
    


print(type(images_path))


for board in os.listdir(boards_path):

    board_path = os.path.join(boards_path,board)
    board_img = Image.open(board_path)

    for index in range(5):
        background = random.choice(os.listdir(backgrounds_path))

        background_path = os.path.join(backgrounds_path,background)

        background_img = Image.open(background_path)
        
        PutBoardToBackground(board_img=board_img, board_name=board, background=background_img, index=int(index))



    #print(f"{board_img.getpixel((928,928))}")


