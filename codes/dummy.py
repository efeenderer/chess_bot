import os
import shutil
import cv2 as cv
import random
from PIL import Image
import screeninfo


monitors = screeninfo.get_monitors()

for index, info in enumerate(monitors):
    print(f"Monitor:{index}  Name:{info.name} Size: {info.width}x{info.height}")
    print(info)




"""
######################################################### Chess Com taş görüntülerinin taş tipi ve boyutuna göre klasörlenmesi


piece_folders = r"E:\Python_Projeler\ComputerVisionProjects\datasets\Chess_bot\Dataset Chess Com Raw"

directory_base = r"E:\Python_Projeler\ComputerVisionProjects\datasets\Chess_bot\Dataset Chess Com by Type PNG"

# İlk Açılacak Klasörler: .\Chess_bot\Dataset Chess Com by Type PNG\{sayi}
# İkinci Açılacak Klasörler: .\Chess_bot\Dataset Chess Com by Type PNG\{sayi}\{piece_type}
#{sayi} = 100,125,150... Dosya isimlerinde yazıp da varsa o konuma dosya atılacak. Yoksa eğer, klasör oluşturulacak.
#{piece_type} = neo,newspaper,marble... Direkt taş tipleri, tiplere göre düzenleme yapılacak artık.

for folder in os.listdir(piece_folders):
    folder_path = piece_folders+"\\"+folder

    for piece in os.listdir(folder_path):
        
        piece_image_name = piece.split(".")[-2]

        piece_type = piece_image_name.split("_")[-3]
        piece_size = piece_image_name.split("_")[-2]
        piece_name = piece_image_name.split("_")[-1]

        d_size = directory_base + "\\" + piece_size

        d_type = d_size + "\\" + piece_type

        

        os.makedirs(d_size,exist_ok=True)
        os.makedirs(d_type,exist_ok=True)
        if not os.path.exists(d_type+"\\"+piece):  
            try: 
                s = os.path.join(folder_path,piece)
                shutil.copy2(s,d_type)
                print(f"Dosya basariyla kopyalandi: {piece}")
            except Exception as e:
                print(f"Aktarilamadi: {piece} Hata: {e} ")
        else:
            print(f"Dosya {piece} zaten konumda mevcut")
"""
        
"""
##################################################################### Chess Com Annotation

piece_ids = {'bp':0,'wp':6,
             'bn':1,'wn':7,
             'bb':2,'wb':8,
             'br':3,'wr':9,
             'bq':4,'wq':10,
             'bk':5,'wk':11}

piece_annotations = {'b':" 0.495550 0.523500 0.931300 0.940200",
                     'p':" 0.496800 0.543900 0.661600 0.856200",
                     'n':" 0.497450 0.491700 0.871500 0.958000",
                     'q':" 0.500000 0.524800 0.958000 0.904600",
                     'r':" 0.502550 0.545800 0.767100 0.867600",
                     'k':" 0.494900 0.511450 0.927400 0.926300"}


image_paths = (r"E:\Python_Projeler\ComputerVisionProjects\datasets\Chess_bot\dataset7 Chess Com\train\images",
               r"E:\Python_Projeler\ComputerVisionProjects\datasets\Chess_bot\dataset7 Chess Com\val\images",
               r"E:\Python_Projeler\ComputerVisionProjects\datasets\Chess_bot\dataset7 Chess Com\test\images")

labels_paths = (r"E:\Python_Projeler\ComputerVisionProjects\datasets\Chess_bot\dataset7 Chess Com\train\labels",
               r"E:\Python_Projeler\ComputerVisionProjects\datasets\Chess_bot\dataset7 Chess Com\val\labels",
               r"E:\Python_Projeler\ComputerVisionProjects\datasets\Chess_bot\dataset7 Chess Com\test\labels")


for image_path,label_path in zip(image_paths,labels_paths):
    for image in os.listdir(image_path):

        image_name = image.split(".")[-2]
        piece_name = image_name.split("_")[-1]

        if not os.path.exists(label_path+"\\"+image_name+".txt"):
            os.path.join(label_path+"\\"+image_name+".txt")
        
        with open(label_path+"\\"+image_name+".txt","w+") as f:
            piece = piece_name[-1]
            TEXT = str(piece_ids[piece_name]) + piece_annotations[piece]
            f.write(TEXT)
            print(TEXT)
"""


"""

########################### Chess COM'dan gelen, jpeg dosyalarının dataset7 dosyasına kopyalanması

directory = [r"E:\Python_Projeler\ComputerVisionProjects\datasets\Chess_bot\dataset7 Chess Com\test\images",
         r"E:\Python_Projeler\ComputerVisionProjects\datasets\Chess_bot\dataset7 Chess Com\val\images",
         r"E:\Python_Projeler\ComputerVisionProjects\datasets\Chess_bot\dataset7 Chess Com\train\images"]
path = r"E:\Python_Projeler\ComputerVisionProjects\datasets\Chess_bot\Dataset Chess Com JPG"

for file in os.listdir(path):
    s = path + "\\" + file
    folder_choice = random.random()
    if folder_choice <= 0.1:
        d = directory[0]
    elif folder_choice <= 0.2:
        d = directory[1]
    else:
        d = directory[2]
    try:
        shutil.copy2(s,d)
        print(f"File: {file} has been successfully copied to direction: {d}")
    except:
        print(f"There's been an error during copying the file {file}")

"""


"""

########################### Chess COM'dan gelen görüntülerin jpeg formata geçirilip rastgele arkaplan atanması

path = r"E:\Python_Projeler\ComputerVisionProjects\datasets\Chess_bot\Dataset Chess Com Raw"

d = r"E:\Python_Projeler\ComputerVisionProjects\datasets\Chess_bot\Dataset Chess Bot JPG"


colors = [(115,149,82),(235,236,208),(42,48,61),(97,130,155),(237,214,176),(184,135,98),(232,240,241),(132,118,186),(240,241,240),(168,169,168),(216,217,216),(206,136,21),(250,224,178)]


for folder in os.listdir(path):
    path2 = path+"\\"+folder
    for file in os.listdir(path2):
        if file.split(".")[-1] == "png":
            s = path2+"\\"+file
            
            image_name = file.split(".")[-2]

            img_png = Image.open(s)

            if img_png.mode != 'RGBA':
                img_png = img_png.convert('RGBA')

            new_image = Image.new("RGB", img_png.size, colors[random.randint(0,len(colors)-1)])
            
            new_image.paste(img_png, (0, 0), img_png)

            output_path = os.path.join(d, f"{image_name}.jpeg")
            
            try:
                new_image.save(output_path, "JPEG")
                print(f"{image_name}.jpeg has been saved to {d}")
            except Exception as e:
                print(f"Couldn't save {file}: {e}")
"""



"""
########################### Chess COM'dan gelen görüntülerin taş tipine göre klasörlenmesi

images_path = r"E:\Python_Projeler\ComputerVisionProjects\datasets\Chess_bot\dataset7 Chess Com\train\images"
dir_path = r"E:\Python_Projeler\ComputerVisionProjects\datasets\Chess_bot\Dataset Chess Com Raw"


for image in os.listdir(images_path):
    
    piece = image.split("_")[-1].split(".")[-2]
    
    if not os.path.exists(dir_path+"\\"+piece):
        os.mkdir(dir_path+"\\"+piece)
    
    s = images_path+"\\"+image
    d = dir_path + "\\" + piece
    try:
        shutil.move(s,d)
        print(f"File: {image} has been successfully moved to direction: {d}")
    except:
        print(f"Error!! {image} couldn't have been moved successfully.")

"""

#os.mkdir(path+"\\"+"wn")

