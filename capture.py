import serial, os, cv2
from affine import Transformer

### Telegram bot
import telegram
import asyncio
token = "6628631471:AAHn0UD7cACVrz7kdTng-XvxYkA1rvBa-Uc"
bot = telegram.Bot(token=token)
chat_id = 6323070063
###

port = '/dev/cu.usbmodem1401'
board = serial.Serial(port, 9600)
cap = cv2.VideoCapture(0)

# 현재 카메라 해상도 얻기
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

# 1440x1440 해상도로 변경 시도
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1440)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)

def isDirExist(cnt):
    if f"try_{N}" not in os.listdir('imgs/'):
        os.mkdir(f"imgs/try_{N}")
        os.mkdir(f"imgs/try_{N}/try_{N}_origin")
        return False
    else:
        return True

def makeImage(image, vol):
    img = cv2.resize(image, dsize=(1440, 1440))
    transformer = Transformer(img)
    centered = transformer.MoveQrToCenter(transformer._image)
    aff = transformer.Affine(centered)
    affrot = transformer.Rotate(aff)

    transformer.reset(affrot)
    constant = transformer.MakeConstantQr(affrot)
    crop = transformer.CropInfusor(constant)

    file = f'./imgs/try_{N}/try_{N}_origin/try_{N}_cap_{vol}.jpeg'
    img = cv2.imwrite(file, crop)

    print(f'{vol} captured!')

# init = 280
init = 277
N = 0
vol = 0
i = 0
start = False



while True:
    if not isDirExist(N):
        break
    else:
        N += 1
    

while True:
    ret, frame = cap.read()    # Read 결과와 frame

    if(ret) :
        cv2.imshow('test', frame)    # 컬러 화면 출력

        try:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                makeImage(frame, 0)
                break

            if board.readable():
                res = board.readline()
                res = float(res.decode())
                print(res)
                if res > 277:
                    start = True
                if start and res <= init - i*10:
                    vol = init - i*10 - 57
                    i += 1
                    makeImage(frame, vol)
                if res < 58.1 and start:
                    makeImage(frame, 0)
                    break

        except:
            vol = init - i*10 - 57
            text = f"[Try {N}]: {vol}mL 촬영에 실패했습니다."
            asyncio.run(bot.sendMessage(chat_id=chat_id, text=text))
            continue

cap.release()
cv2.destroyAllWindows()
text = f"[Try {N}]: 촬영이 종료됐습니다."
asyncio.run(bot.sendMessage(chat_id=chat_id, text=text))