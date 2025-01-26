import os
import random
import shutil


def getFilePath():
    file_path = os.path.dirname(__file__)

    return file_path[0].upper() + file_path[1:]

def UpperPath(path): #Upper folder of the argument "path"
    upper_path = os.path.dirname(path)

    return upper_path[0].upper() + upper_path[1:]

__path__ = getFilePath()    #Directory of the current file

paths = [os.path.join(UpperPath(UpperPath(__path__)), "dataset\\board_set"+"\\"+path) for path in ['train','val','test']]

images_paths = [os.path.join(path,"images") for path in paths]

labels_paths = [os.path.join(path,"labels") for path in paths]

def shuffle_files(images_path, labels_path):
    image_files = os.listdir(images_path)
    label_files = os.listdir(labels_path)
    
    # Dosya adlarını ve uzantılarını ayır
    file_names_and_extensions = [os.path.splitext(file) for file in image_files]
    
    # Yeni rastgele isimler oluştur
    new_names = [f"{i:06d}" for i in range(len(file_names_and_extensions))]
    random.shuffle(new_names)
    
    # Dosyaları yeniden adlandır
    for (old_name, extension), new_name in zip(file_names_and_extensions, new_names):
        # Görüntü dosyasını yeniden adlandır
        old_image_path = os.path.join(images_path, old_name + extension)
        new_image_path = os.path.join(images_path, new_name + extension)
        shutil.move(old_image_path, new_image_path)
        
        # Etiket dosyasını yeniden adlandır
        old_label_path = os.path.join(labels_path, old_name + ".txt")
        new_label_path = os.path.join(labels_path, new_name + ".txt")
        shutil.move(old_label_path, new_label_path)
        
        print(f"Renamed: {old_name}{extension} to {new_name}{extension}")

# Her bir klasör çifti için işlemi gerçekleştir
for images_path, labels_path in zip(images_paths, labels_paths):
    print(f"Processing: {images_path} and {labels_path}")
    shuffle_files(images_path, labels_path)
    print("Finished processing this pair of folders.\n")
