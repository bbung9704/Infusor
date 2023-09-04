import serial
import cv2
import time

port = '/dev/cu.usbmodem1401'
board = serial.Serial(port, 9600)

cap = cv2.VideoCapture(0)
init = 277
# init = 280
i = 0
cnt = 5
start = False
print('width :%d, height : %d' % (cap.get(3), cap.get(4)))

while(True):
    ret, frame = cap.read()    # Read 결과와 frame

    if(ret) :
        cv2.imshow('test', frame)    # 컬러 화면 출력

        if cv2.waitKey(1) & 0xFF == ord('q'):
            img = cv2.imwrite('imgs/0/cap_%d.png' % cnt, frame)
            break

        if board.readable():
            res = board.readline()
            res = float(res.decode())
            print(res)
            if res > 277:
                start = True
            if start and res <= init - i*20:
                vol = init - i*20 - 57
                i += 1
                file = 'imgs/%d/cap_%d.png' % (vol, cnt)
                img = cv2.imwrite(file, frame)
                print('%d captured!' % vol)
                time.sleep(0.5)

            
cap.release()
cv2.destroyAllWindows()