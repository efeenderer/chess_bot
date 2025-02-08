import os
import shutil
import cv2 as cv
import random
from PIL import Image
from stockfish import Stockfish as sf
import screeninfo

stockfish = sf(path=r"E:\Python_Projeler\ComputerVisionProjects\chess_bot\codes\stockfish\stockfish-windows-x86-64-avx2.exe")

stockfish.set_fen_position("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1")

print(stockfish.get_best_move())
