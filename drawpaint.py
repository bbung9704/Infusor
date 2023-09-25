# packages
import cv2, os

N = 0
root = f"imgs/try_{N}/try_{N}_filled/"
files = os.listdir(root)

if f"try_{N}_paint" not in os.listdir(f"imgs/try_{N}"):
    os.mkdir(f"imgs/try_{N}/try_{N}_paint")

for file in files:
    img = cv2.imread(root + file, cv2.IMREAD_GRAYSCALE)

    # init a canvas
    canvas = img

    # global coordinates and drawing state
    x = 0
    y = 0
    drawing = False

    # mouse callback function
    def draw(event, current_x, current_y, flags, params):
        # hook up global variables
        global x, y, drawing
        
        # handle mouse down event
        if event == cv2.EVENT_LBUTTONDOWN:
            # update coordinates
            x = current_x
            y = current_y
            
            # enable drawing flag
            drawing = True
        
        # handle mouse move event
        elif event == cv2.EVENT_MOUSEMOVE:
            # draw only if mouse is down
            if drawing:
                # draw the line
                cv2.line(canvas, (current_x, current_y), (x, y), 0, thickness=30)
                
                # update coordinates
                x, y = current_x, current_y
        
        # handle mouse up event
        elif event == cv2.EVENT_LBUTTONUP:
            # disable drawing flag
            drawing = False
        


    # display the canvas in a window
    cv2.imshow('Draw', canvas)

    # bind mouse events
    cv2.setMouseCallback('Draw', draw)

    # infinite drawing loop
    while True:
        # update canvas
        cv2.imshow('Draw', canvas)
        
        # break out of a program on 'Esc' button hit
        if cv2.waitKey(1) & 0xFF == 27:
            cv2.imwrite(f"imgs/try_{N}/try_{N}_paint/" + file, canvas)
            break

# clean up windows
cv2.destroyAllWindows()



