import os
import mss
from ultralytics import YOLO
import cv2 as cv
import numpy as np
from PIL import Image
from stockfish import Stockfish
import time as t
from screeninfo import get_monitors
import copy



monitor = {"top": 0, "left": 0, "width": int(get_monitors()[0].width), "height": int(get_monitors()[0].height)}
sct = mss.mss()

def getFilePath():
    file_path = os.path.dirname(__file__)

    return file_path[0].upper() + file_path[1:]
def UpperPath(path):
    upper_path = os.path.dirname(path)

    return upper_path[0].upper() + upper_path[1:]
__path__ = getFilePath()

stockfish = Stockfish(path = __path__+r"\stockfish\stockfish-windows-x86-64-avx2.exe")

piece_by_id = {0:'p',6:'P',
               1:'n',7:'N',
               2:'b',8:'B',
               3:'r',9:'R',
               4:'q',10:'Q',
               5:'k',11:'K'}

piece_by_side = {'w':['P','N','B','R','Q','K'],
                 'b':['p','n','b','r','q','k']}

piece_map = [[0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0]]

coordinates = [0.0625, .1875, .3125, .4375, .5625, .6875, .8125, .9375]

castling = {'w':"KQ",'b':"kq"}

def DetectBoard():
    try:
        #screenshot = np.array(sct.grab(monitor))
        screenshot = np.array(sct.grab(monitor))
        frame = np.array(screenshot)
        frame = cv.cvtColor(screenshot,cv.COLOR_RGB2BGR)
                        
        results = board_model(frame,verbose=False)

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

        results = piece_model(board,conf=0.8,verbose=False)
        
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

def Detection():
    while True:
        board_crop = DetectBoard()
        if board_crop is None:
            t.sleep(0.1)
            continue
        DetectPieces(board=board_crop) 
        break

def ShowBoard(piece_map=None):
    if piece_map is None:
        Detection()
    
    for row in piece_map:
        for piece in row:
            if piece == 0:
                print(f"  ",end="")
                continue
            print(f"{piece} ",end="")
        print()

def ImageTests(): 

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

def BestMove(FEN):
    try:
        if stockfish.is_fen_valid(FEN):
            print("FEN is Valid")
            stockfish.set_fen_position(FEN)

            best_move = stockfish.get_best_move()
            square = best_move[:2]
            
            moved_piece = stockfish.get_what_is_on_square(square=square)
            
            evaluation = stockfish.get_evaluation()

            print(f"\nEvaluation: {evaluation}")
            
            print(f"\nBest Move: {best_move}\n")
            return best_move
        else:
            raise Exception("Error: FEN is not Valid")
    except Exception as e:
        print(f"There's been an error finding the best move: {e}")

def Reset():
    castling = "KQkq"
    for row in range(8):
        for column in range(8):
            piece_map[int(row)][int(column)] = 0

def FindFEN(turn="w", enPassant = "-", user_side = None):
    try: 
        castle = castling['w']+castling['b']
        ShowBoard(piece_map)
        
        board_map = copy.deepcopy(piece_map) 

        FEN = ""

        piece_notation = ""

        if user_side == "b":
            board_map = [row[::-1] for row in board_map[::-1]]

        for index,row in enumerate(board_map):
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
        FEN += turn + " "
        FEN += castle + " "
        FEN += enPassant + " 0 1"
        

        print(f"FEN = {FEN}")
        return FEN

    except Exception as E:
        print(f"There was an error detecting FEN.    Error: {E}")

def MovePiece():
    return

def GetMovedPiece(piece_map, piece_map_memory, side):         #It still is not good. If the user dont follow the rules, this functions blows up.
    
    other_side = 'w' if side == 'b' else 'b'

    for row in range(8):
        for column in range(8):
            if piece_map[row][column] != piece_map_memory[row][column]:  #This one checks if there's a difference between two maps
                if piece_map_memory[row][column] in piece_by_side[side]:  # Moved piece is opponent's.
                    if piece_map[row][column] not in piece_by_side[other_side]: # There's an opponent piece or there's nothing in the old place of the moved piece
                        moved_piece = piece_map_memory[row][column] 
                        print(f"\nMoved Piece is {moved_piece}")
                        return moved_piece
    return

def WaitForTurn(opponent_side):
    piece_map_memory = copy.deepcopy(piece_map)

    while True:
        try:
            Reset()
            board_crop = DetectBoard()
            DetectPieces(board=board_crop)
            
            """
            print("Current map")
            ShowBoard(piece_map)
            print("Memory map")
            ShowBoard(piece_map_memory)
            """

            if piece_map == piece_map_memory:      #Since the map is a list matrix size of 8x8, this check is more than enough.
                t.sleep(1)
                continue
            moved_piece = GetMovedPiece(piece_map,piece_map_memory,opponent_side)

            if moved_piece in piece_by_side[opponent_side]:
                return
        except Exception as e:
            print(f"There's been an error during waiting for turn.       Error:{e}")
        
def MenuLoop():
    print("Chess Bot is ready. Type 'help' for commands.")
    while True:
        print()
        command = input(">>> ").strip().lower()
        if command == "quit":
            print("Exiting Chess Bot.")
            t.sleep(0.5)
            t.sleep(0.2)
            break
        elif command == "help":
            print(" - start middle: Starts the bot for an ongoing game")
            print(" - start new: Starts the bot for a new game")
            print(" - start puzzle: Starts the bot for a puzzle")
            print(" - show: Display the current board.")
            print(" - quit: Exit the bot.")
            t.sleep(0.5)
            continue
        elif command == "start new" or command == "start middle" or command == "start puzzle":
            print("The Game is getting started...\n\n")
            BotLoop(command.split(" ")[-1])
            t.sleep(0.5)
            continue

        elif "start" in command:
            print("You should type \"start new\" or \"start middle\"")
            t.sleep(0.5)
            continue

        elif "reset" in command:
            Reset()
            t.sleep(0.5)
            continue
        elif "show" in command:
            ShowBoard()
            t.sleep(0.2)
            continue

        elif "test" in command:
            BotLoop("new")
            t.sleep(0.5)
            continue
  
def BotLoop(gameType):
    if gameType == "new":
        print("Waiting for chess board...")
        Detection()
        t.sleep(0.5)
        
        player_side = "b" if piece_map[0][0] == "R" else "w"
        opponent_side = "b" if player_side == "w" else "w"
        whose_turn = 'w'
        FindFEN(user_side=player_side)
        print(f"\nUser is {'black' if player_side=='b' else 'white'}")
        t.sleep(0.1)
        print(f"\nOpponent {'black' if opponent_side=='b' else 'white'}")

        t.sleep(1)
        while True:
            try:
                
                print(f"IT'S {'black' if whose_turn=='b' else 'white'} side's turn ")

                if whose_turn == player_side:
                    try:
                        whose_turn = opponent_side
                        BestMove(FindFEN(turn=player_side,user_side=player_side))

                    except Exception as e:
                        print(f"Error in BotLoop, GameType: {gameType}      Error: {e}") 
                        choice = input()
                        if choice == "99":
                            quit(1)

                elif whose_turn == opponent_side:
                    WaitForTurn(opponent_side)
                    whose_turn = player_side
                else: raise Exception
            except:
                print("There's something wrong with turn detection.")

    elif gameType == "puzzle":
        print("Waiting for chess board...")
        Detection()
        FindFEN()
        while True:
            return
    elif gameType == "middle":

        castling_rights = {"KQkq", "KQk", "KQq", "Kkq", "Kq", "Kk", "Qkq", "Qq", "Qk", "K", "Q","k","q","kq","-"}

        

        while True: 
            print("Which Sides are suitable for castling? Type the sides in form of \"KQkq\". ")
            isItCastled = input(">>>")
            
            if isItCastled in castling_rights:
                print("Which side are you? (w/b)")
                whichSide = input(">>> ").strip().lower()
                Detection()
                print("Waiting for chess board...")
                firstFEN = FindFEN(castle=isItCastled, turn=whichSide)

                if stockfish.is_fen_valid(firstFEN):
                    pass                                                #Buradan devam edecek

            else:
                print("\nType the Castling correctly!\n")


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


        




