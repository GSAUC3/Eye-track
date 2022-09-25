from numpy import interp
import cv2 
import mediapipe as mp 
import pyautogui as pg 

Width,Height = pg.size()

cap = cv2.VideoCapture(0)
vw,vh = 640,480
pg.FAILSAFE = False
cx = px = cy = py = 0

faceMesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

FACTOR = 3
ORIGIN = (220, 150)
SMOOTHIE = 0.2

centerx=centery=0
firstRun = True
while 1:
    _, img = cap.read()

    img = cv2.flip(img,1)
    rgbImg = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = faceMesh.process(rgbImg)
    landmarks = results.multi_face_landmarks # this of type list withlen 1
    # type(landmarks[0]) == <class 'mediapipe.framework.formats.landmark_pb2.NormalizedLandmarkList'>
    height,width,_ = img.shape
    # print(type(landmarks[0].landmark[474:478]))
    # ids = [145,159,475,477]
    lefteye = [33,133]#,263,362
    if landmarks:
        l=landmarks[0].landmark[145]
        l1=landmarks[0].landmark[159]
        x,y = (l.x*width),(l.y*height)
        x1,y1 = (l1.x*width),(l1.y*height)
        centerx,centery=(x+x1)//2,(y+y1)//2
        cv2.circle(img,(int(centerx),int(centery)),1,(255,0,255))
        if firstRun:
            ORIGIN = (int(centerx-32),int(centery-18))
            firstRun=False
        cv2.rectangle(img, ORIGIN, (ORIGIN[0]+16*FACTOR, ORIGIN[1]+9*FACTOR), (0, 255, 255), 1)
        centerx = interp(centerx, (ORIGIN[0], ORIGIN[0]+16*FACTOR), (0, 1920))
        centery = interp(centery, (ORIGIN[1], ORIGIN[1]+9*FACTOR), (0, 1080))
        cx = px + (centerx-px)*SMOOTHIE
        cy = py + (centery-py)*SMOOTHIE
        # current location = (new location -past location)/factor
        if x < width and y < height:
            pg.moveTo(cx, cy)
        px,py = cx,cy

    cv2.imshow('Output',img)
    if cv2.waitKey(1)==27:
        break

cap.release()
cv2.destroyAllWindows()