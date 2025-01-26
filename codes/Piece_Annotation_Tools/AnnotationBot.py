import os

def getFilePath():
    file_path = os.path.dirname(__file__)

    return file_path[0].upper() + file_path[1:]

def UpperPath(path): #Upper folder of the argument "path"
    upper_path = os.path.dirname(path)

    return upper_path[0].upper() + upper_path[1:]

__path__ = getFilePath()    #Directory of the current file


paths = [os.path.join(UpperPath(UpperPath(__path__)),"dataset\\All_sets"+"\\"+path) for path in ['val','train','test'] ]

images_paths = [os.path.join(path,"images") for path in paths]
labels_paths = [os.path.join(path,"labels") for path in paths]

def AnnotationFEN():
    pieces = {'p':0,'n':1,'b':2,'r':3,'q':4,'k':5,'P':6,'N':7,'B':8,'R':9,'Q':10,'K':11}


    for images_path,labels_path in zip(images_paths,labels_paths):
        file_names = []
        file = os.listdir(images_path)

        for names in file:
            file_name_list = []
            file_name = ""
            for letter in names:
                if letter == "-":
                    file_name_list.append(file_name)
                    file_name = ""
                    continue
                if letter == ".":
                    file_name_list.append(file_name)
                    break
                file_name = file_name + letter
            file_names.append(file_name_list)

        print(len(file_names))
        print(len(file))

        box_widths = {'p':[0.0885, 0.115175],'P':[0.0885, 0.115175],
                    'n':[0.1045, 0.10805],'N':[0.1045, 0.10805],
                    'b':[0.1041, 0.105825],'B':[0.1041, 0.105825],
                    'r':[0.0891, 0.10325],'R':[0.0891, 0.10325],
                    'q':[0.11225, 0.1064],'Q':[0.11225, 0.1064],
                    'k':[0.105, 0.111375],'K':[0.105, 0.111375]}

        center_offsets = {'p':[0.00015, 0.00491],'P':[0.00015, 0.00491],
                        'n':[0.00145 ,0.001075],'N':[0.00145 ,0.001075],
                        'b':[0.00045, 0.000713],'B':[0.00045, 0.000713],
                        'r':[-0.00025, 0.00475],'R':[-0.00025, 0.00475],
                        'q':[0.000812, 0.000475],'Q':[0.000812, 0.000475],
                        'k':[0.000175, -0.001312],'K':[0.000175, -0.001312]}

            
        for index in range(len(file_names)):

            if not os.path.exists(labels_path+"\\"+file[index].split(".")[-2]+".txt"):
                os.path.join(labels_path,file[index].split(".")[-2]+".txt")

            with open(labels_path+r"\\"+file[index].split(".")[-2]+".txt","w+") as dosya:
                name = file_names[index]
                y = 0
                while y < 8:
                    x = 0
                    for letter in name[y]:
                        if str(letter).isdigit():
                            x = x + int(letter)
                            continue
                        center_y = 0.0625*(2*y+1)
                        center_x = 0.0625*(2*x+1)
                        x = x+1
                        TEXT = f"{pieces[letter]} {center_x + center_offsets[letter][0] } {center_y + center_offsets[letter][1]} {box_widths[letter][0]} {box_widths[letter][1]}\n"
                        dosya.write(TEXT)
                    y = y+1
                dosya.close()
            print(file[index].split(".")[-2]+".txt"+" is created at: "+ labels_path + " "+str(index+1)+"/"+str(len(file)))
    
            

if __name__ == "__main__":
    AnnotationFEN()