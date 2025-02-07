import os
import mss
from ultralytics import YOLO
import cv2 as cv
import numpy as np
from PIL import Image
from stockfish import Stockfish
import time as t
from screeninfo import get_monitors


monitor = {"top": 0, "left": 0, "width": int(get_monitors()[0].width), "height": int(get_monitors()[0].height)}
sct = mss.mss()

"""try:
        sct = mss.mss()
except Exception as e:
    print(f"There was an error creating sct. Error: {e}")"""

def getFilePath():
    file_path = os.path.dirname(__file__)

    return file_path[0].upper() + file_path[1:]
def UpperPath(path):
    upper_path = os.path.dirname(path)

    return upper_path[0].upper() + upper_path[1:]

__path__ = getFilePath()


piece_by_id = {0:'p',6:'P',
               1:'n',7:'N',
               2:'b',8:'B',
               3:'r',9:'R',
               4:'q',10:'Q',
               5:'k',11:'K'}

piece_map = [[0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0]]


coordinates = [0.0625, .1875, .3125, .4375, .5625, .6875, .8125, .9375]
             
#Piece Map will look like this:
#[[p,p,p,p,p,0,0,0],
# [b,B,0,0,0,0,0,0],
# .................
# .................
# .................
# ......,K,Q,0,0,R]] Obiviously, they're all gonna be chars




"""
def Screenshot():
    with mss.mss() as sct:          #I kept getting this error: AttributeError: '_thread._local' object has no attribute 'srcdc'. Don't know why but getting screenshots this way solved that problem. 
        return sct.grab(monitor)    #I'll work on that later to see what was the problem
    """


def DetectBoard():
    try:
        #screenshot = np.array(sct.grab(monitor))
        screenshot = np.array(sct.grab(monitor))
        frame = np.array(screenshot)
        frame = cv.cvtColor(screenshot,cv.COLOR_RGB2BGR)
        #frame = cv.resize( frame , ( 1184 , 666 ) )                TI
                        
        results = board_model(frame)

        boxes = results[0].boxes
        
        if len(boxes) > 0:
            box = boxes[0].xyxy[0]
            x1,y1,x2,y2 = map(int,box)
            board = frame[y1:y2,x1:x2]
            return board
        
    except Exception as e:
        print(f"Error in detect_board: {e}")

    return None


def ClosestCoordinate(center):

    lowest_difference = abs(coordinates[0] - center)
    i = 0

    for index, coordinate in enumerate(coordinates):
        #print(f"Coordinate = {coordinate}")
        current_difference = abs(coordinate - center)
        if lowest_difference > current_difference:
            i = index
            lowest_difference = current_difference

    return coordinates[i]
            


def DetectPieces(board):
    try:
        if board is None:
            return
        #print(f"\n\nboard.shape[0:-2]= {board.shape[0:-2]}\n board.shape={board.shape}\n\n")
        board_size_x = board.shape[0]
        board_size_y = board.shape[1]

        results = piece_model(board,conf=0.8)
        
        i = 0
        for box in results[0].boxes:
            
            piece = piece_by_id[int(box.cls)]
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            center_x = ( (x1+x2)/ ( 2 * board_size_x) )
            center_y = ( (y1+y2)/ ( 2 * board_size_y) )
            #print(f"\n\nbox: {piece}\nx,y = {center_x},{center_y}\n\n")
            center_x = ClosestCoordinate(center_x)
            center_y = ClosestCoordinate(center_y)

            column = int((center_x - 0.0625)/.125)
            row = int((center_y - 0.0625)/.125)

            piece_map[row][column] = piece
            #print(f"\n\nbox: {piece}\nx,y = {center_x},{center_y}\n\n")
            

    except Exception as E:
        print(f"Error in detecting pieces.     Error: {E}")
        

def ShowBoard():
    for row in piece_map:
        for piece in row:
            if piece == 0:
                print(f"  ",end="")
                continue
            print(f"{piece} ",end="")
        print()


def Tests(): 

    cv.namedWindow("test",cv.WINDOW_NORMAL)

    while True: #main loop
        try:
            #ALL CHOICE FLAG VARIABLES WILL START WITH "_"
            
            board_crop = DetectBoard()
            image_pieces = np.zeros((500,500,3), np.uint8)
            if board_crop is not None:
                image_pieces = DetectPieces(board_crop)
            
            cv.imshow("test",image_pieces)

            if cv.waitKey(1) & 0xFF == ord('q'):
                break
            
        except Exception as e:
            print(f"An Error occured, Error:{e}")
        t.sleep(0.1)



def FindFEN(castle="KQkq",turn="w", enPassant = "-"):
    try: 
        board_crop = DetectBoard()
        DetectPieces(board=board_crop)
        
        ShowBoard()
        FEN = ""

        piece_notation = ""

        for index,row in enumerate(piece_map):
            empty = 0
            for piece in row:
                if piece == 0:
                    empty += 1
                    continue
                if empty > 0:
                    piece_notation += str(empty)
                piece_notation += piece
                empty = 0

            if empty > 0:
                piece_notation += str(empty)
            if index != 7:
                piece_notation += "/"

        FEN += piece_notation + " "
        FEN += castle + " "
        FEN += turn + " "
        FEN += enPassant + " 0 1"
        

        print(f"FEN = {FEN}")

    except Exception as E:
        print(f"There was an error detecting FEN.    Error: {E}")

def MovePiece():
    return

def MenuLoop():
    print("Chess Bot is ready. Type 'help' for commands.")
    while True:
        print()
        command = input(">>> ").strip().lower()
        if command == "quit":
            print("Exiting Chess Bot.")
            t.sleep(0.2)
            break
        elif command == "help":
            print(" - start middle: Starts the bot for an ongoing game")
            print(" - start new: Starts the bot for a new game")
            print(" - start puzzle: Starts the bot for a puzzle")
            print(" - show: Display the current board.")
            print(" - quit: Exit the bot.")
        elif command == "start new" or command == "start middle" or command == "start puzzle":
            print("The Game is getting started...\n\n")
            BotLoop(command.split(" ")[-1])

        elif "start" in command:
            print("You should type \"start new\" or \"start middle\"")
            continue
        elif command == "reset":
            for row in range(8):
                for column in range(8):
                    piece_map[int(row)][int(column)] = 0
        elif command == "test":
            FindFEN()
        
            
def BotLoop(gameType):
    if gameType == "new":
        FindFEN()
        while True:
            return
    elif gameType == "puzzle":
        FindFEN()
        while True:
            return






if __name__ == "__main__":
    board_model = YOLO(os.path.join(__path__,'models\\board_model.pt'), verbose=False)
    piece_model = YOLO(r"E:\Python_Projeler\ComputerVisionProjects\chess_bot\codes\models\piece_model.pt", verbose=False)


    print("\n\n")                          
    print("♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖")         # Need a little show off, right?
    t.sleep(0.05)
    print("♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙")
    t.sleep(0.05)
    print("================")
    t.sleep(0.05)
    print("WELCOME TO THE")
    t.sleep(0.05)
    print("CHESS BOT")
    t.sleep(0.05)
    print("================")
    t.sleep(0.05)
    print("♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙")
    t.sleep(0.05)
    print("♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖")
    t.sleep(0.05)
    print("\n\n")

    MenuLoop()

    print("\n\n")
    print("♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖")
    t.sleep(0.05)
    print("♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙")
    t.sleep(0.05)
    print("================")
    t.sleep(0.05)
    print("==  GOODBYE  ==")
    t.sleep(0.05)
    print("================")
    t.sleep(0.05)
    print("♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙")
    t.sleep(0.05)
    print("♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖")
    t.sleep(0.05)
    print("\n\n")


            




