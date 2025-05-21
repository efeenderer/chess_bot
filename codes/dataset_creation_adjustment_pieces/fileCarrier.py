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

path = r"DATASET_THAT_WILL_BE_COPIED"
dst_path = [r"COPY_LOCATION_test",
            r"COPY_LOCATION_val",
            r"COPY_LOCATION_train"]

try:
    images_path = os.path.join(path, "images")
    labels_path = os.path.join(path, "labels")
except Exception as e:
    print(f"Olmadi {e}")

for dst in dst_path:
    os.makedirs(os.path.join(dst, "labels"), exist_ok=True)
    os.makedirs(os.path.join(dst, "images"), exist_ok=True)


image_files = sorted(os.listdir(images_path))
label_files = sorted(os.listdir(labels_path))


file_pairs = list(zip(image_files, label_files))

for index, (image, label) in enumerate(file_pairs):
    which_path = random.random()

    if which_path <= .10:
        dst = dst_path[0]  # test'e gönder
    elif which_path <= .20:
        dst = dst_path[1]  # val'a gönder
    else:
        dst = dst_path[2]  # train'e gönder

    try:
        src_image = os.path.join(images_path, image)
        dst_image = os.path.join(dst, "images", image)
        shutil.copy2(src_image, dst_image)
        print(f"{image} basariyla tasindi: {dst_image}  ------ {index+1}/{len(file_pairs)}")

        src_label = os.path.join(labels_path, label)
        dst_label = os.path.join(dst, "labels", label)
        shutil.copy2(src_label, dst_label)
        print(f"{label} basariyla tasindi: {dst_label}  ------ {index+1}/{len(file_pairs)}")
    except Exception as e:
        print(f"{image} veya {label} tasinirken hata olustu: {e}")


for dst in dst_path:
    image_count = len(os.listdir(os.path.join(dst, "images")))
    label_count = len(os.listdir(os.path.join(dst, "labels")))
    print(f"{dst}: {image_count} görüntü, {label_count} etiket")

total_images = sum(len(os.listdir(os.path.join(dst, "images"))) for dst in dst_path)
total_labels = sum(len(os.listdir(os.path.join(dst, "labels"))) for dst in dst_path)
print(f"Toplam: {total_images} görüntü, {total_labels} etiket")