import os
from ultralytics import YOLO
import cv2 as cv
import numpy as np
from PIL import Image
from stockfish import Stockfish

# Stockfish'in tam yolu (raw string olarak yazdım)


import pyautogui

def capture_screen():
    screenshot = pyautogui.screenshot()
    return cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)


def getFilePath():
    file_path = os.path.dirname(__file__)

    return file_path[0].upper() + file_path[1:]
def UpperPath(path):
    upper_path = os.path.dirname(path)

    return upper_path[0].upper() + upper_path[1:]

__path__ = getFilePath()

stockfish = Stockfish(os.path.join(__path__,r"\stockfish\stockfish-windows-x86-64-avx2.exe"))

FEN_ID = {0:'p',6:'P',
          1:'n',7:'N',
          2:'b',8:'B',
          3:'r',9:'R',
          4:'q',10:'Q',
          5:'k',11:'K'}

def detectBoard(image_path):
    try:
        image = cv.imread(image_path)
        image = cv.cvtColor(image,cv.COLOR_RGB2BGR)

        results = board_model(image)

        boxes = results[0].boxes

        if len(boxes) > 0:
            box = boxes[0].xyxy[0]
            x1,y1,x2,y2 = map(int,box)
            board = image[y1:y2,x1:x2]
            return board

    except Exception as e:
        print(f"Board Detect edilemedi {e}")
        return None
    

def detectPieces(image):
    try: 
        if image is None:
            return None, []
        
        results = piece_model(image)
        print(f"Size of Board: {image.shape}")
        
        pieces = []
        
        for box in results.boxes:
            class_id = int(box.cls)
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2) 
            pieces.append((class_id, (center_x, center_y)))
        
        detection_image = results.plot(font_size=5)
        return cv.cvtColor(detection_image, cv.COLOR_RGB2BGR), pieces

    except Exception as e:
        print(f"Taşlar tespit edilemedi: {e}")
        return None, []



def showWindow(image_path):
    
    image = detectBoard(image_path=image_path)
    image = detectPieces(image)
    while True:
        try:
            if image is None: 
                print("Goruntu Gelmedi")
                break
            if cv.waitKey(1) & 0xFF ==ord('q'):
                break
            cv.namedWindow("Image")
            cv.imshow("Image",image)
        except Exception as e:
            print(f"Goruntu olusurken HATA: {e}")

    
def processImage():
    test_images = os.path.join(__path__, "Test_Images")
    
    for test_image in os.listdir(test_images):
        path = os.path.join(test_images, test_image)
        print(f"İşlenen görüntü: {path}")
        
        board = detectBoard(path)
        if board is not None:
            detected_image, pieces = detectPieces(board)
            if detected_image is not None and pieces:
                print(f"Tespit edilen taş sayısı: {len(pieces)}")
                
                # FEN oluşturma
                fen = findFEN(pieces, board.shape[:2])
                print(f"FEN: {fen}")
                
                # En iyi hamleyi bulma
                best_move = get_best_move(fen)
                print(f"En iyi hamle: {best_move}")
            
                # Tespit edilen taşları gösteren görüntüyü gösterme
                cv.imshow("Detected Pieces", detected_image)
                cv.waitKey(0)  # Kullanıcı bir tuşa basana kadar bekle
            else:
                print("Taşlar tespit edilemedi veya görüntü işlenemedi.")
        else:
            print("Satranç tahtası tespit edilemedi.")

    cv.destroyAllWindows()





def findFEN(pieces, board_size):

    FEN = ""
    threshold = 0.08
    board_size_x = board_size[0]
    board_size_y = board_size[1]


    for row in range(8):
        number=0
        
        for column in range(8):
            square = (0.0625*(2*int(column)+1), 0.0625*(2*int(row)+1))
            piece_flag = False
            #print(f"x: {square[0]} y: {square[1]}")
            for piece in pieces:

                center_x = piece[1][0]/board_size_x <= square[0] + threshold and piece[1][0]/board_size_x >= square[0] - threshold
                center_y = piece[1][1]/board_size_y <= square[1] + threshold and piece[1][1]/board_size_y >= square[1] - threshold
                
                if center_x and center_y:
                    piece_flag = True
                    if number != 0:
                        FEN = FEN + f"{number}{FEN_ID[piece[0]]}"
                        number = 0
                        break
                    FEN = FEN + f"{FEN_ID[piece[0]]}"
                    break
            if not piece_flag:
                number = number + 1
        if number != 0:
            FEN = FEN + f"{number}"
        FEN = FEN + "/"
    FEN = FEN[:-1]  # Son '/' karakterini kaldır
    
    # Hamle sırası (varsayılan olarak beyaz)
    FEN += " w"
    
    # Rok hakları (varsayılan olarak tüm haklar mevcut)
    FEN += " KQkq"
    
    # Geçerken alma hedefi (varsayılan olarak yok)
    FEN += " -"
    
    # Yarım hamle sayacı ve tam hamle sayısı (varsayılan olarak 0 ve 1)
    FEN += " 0 1"
    print(FEN)
    return FEN
        
def get_best_move(fen):
    stockfish.set_fen_position(fen)
    best_move = stockfish.get_best_move()
    return best_move



if __name__ == '__main__':
    board_model = YOLO(os.path.join(__path__,'models\\board_model.pt'))
    piece_model = YOLO(os.path.join(__path__,'models\\piece_model.pt'))
    processImage()



