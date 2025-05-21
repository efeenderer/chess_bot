import os

def getFilePath():
    file_path = os.path.dirname(__file__)

    return file_path[0].upper() + file_path[1:]

def UpperPath(path): #Upper folder of the argument "path"
    upper_path = os.path.dirname(path)

    return upper_path[0].upper() + upper_path[1:]

__path__ = getFilePath()    #Directory of the current file

paths = [os.path.join(UpperPath(UpperPath(__path__)), "dataset\\dataset5_Negative Set"+"\\"+path) for path in ['train','val','test']]

images_paths = [os.path.join(path,"images") for path in paths]

labels_paths = [os.path.join(path,"labels") for path in paths]



for images_path, labels_path in zip(images_paths,labels_paths):
    
    files = os.listdir(images_path)
    file_names = [file[:-4] for file in files]
    print(labels_path)
    for index,file_name in enumerate(file_names):
        
        label_file_path = os.path.join(labels_path, file_name + ".txt")
        
        # Eğer dosya oluşturmak istiyorsanız:
        if not os.path.exists(label_file_path):
            print(str(index+1) + "/" + str(len(file_names)) + " of files are created. File name: "+ file_names[index])
            with open(label_file_path, 'w') as f:
                continue
                pass  # Boş dosya oluştur
        print(str(index+1) + "/" + str(len(file_names)) + " file is already created. File name: "+ file_names[index])