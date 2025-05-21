import os
import shutil
import cv2 as cv
import random
import numpy as np
from PIL import Image
from stockfish import Stockfish as sf
import screeninfo


def getFilePath():
    file_path = os.path.dirname(__file__)

    return file_path[0].upper() + file_path[1:]
def UpperPath(path):
    upper_path = os.path.dirname(path)

    return upper_path[0].upper() + upper_path[1:]
__path__ = getFilePath()

sizes = np.linspace(125,125,1)
print(sizes)

quit(1)

stockfish = sf(path = __path__+r"\stockfish\stockfish-windows-x86-64-avx2.exe")

castling = "KQkq"

print(castling[-2:])

