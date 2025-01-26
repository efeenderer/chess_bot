import os
import shutil



paths = [r"ALL_DIRECTORIES_FOR_DATASET_PARTS",
         r"ALL_DIRECTORIES_FOR_DATASET_PARTS",
         r"ALL_DIRECTORIES_FOR_DATASET_PARTS",
         r"ALL_DIRECTORIES_FOR_DATASET_PARTS",
         r"ALL_DIRECTORIES_FOR_DATASET_PARTS",
         r"ALL_DIRECTORIES_FOR_DATASET_PARTS"]

destination = r"MAIN_DATASET_DIRECTORY"

for path in os.listdir(destination):
    full_path = os.path.join(destination, path)
    if os.path.isfile(full_path):
        os.remove(full_path)
    elif os.path.isdir(full_path):
        shutil.rmtree(full_path)


for path in paths:
    if path == r"DATASET3_SHOULDNT_BE_INVOLVED":
        continue
    for folder in os.listdir(path):
        s = path+"\\"+folder
        d = destination+"\\"+folder

        if not os.path.exists(d):
            os.path.join(d)
        
        try:
            if os.path.isdir(s):
                shutil.copytree(s,d,dirs_exist_ok=True)
            else:
                shutil.copy2(s,d)
        except shutil.SameFileError:
            print("Source and destination represents the same file.")
        except PermissionError:
            print("Permission denied.")
        except:
            print("Error occurred while copying file.")
    






