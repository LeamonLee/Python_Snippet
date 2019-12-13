import cv2
import ctypes
from screeninfo import get_monitors

# Method1
for m in get_monitors():
    print(str(m))

# Method2
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
maxWidth, maxHeight = screensize
print("maxWidth, maxHeight", maxWidth, maxHeight)

#print("Before URL")
cap = cv2.VideoCapture('rtsp://pioneerm:pioneerm1188@10.101.100.152:554/videoMain')
#print("After URL")

while True:

    #print('About to start the Read command')
    ret, frame = cap.read()

    width, height = frame.shape[:2]
    print("width, height", width, height)

    resized_image = cv2.resize(frame, (maxWidth, maxHeight)) # for example

    width, height = resized_image.shape[:2]
    print("width, height", width, height)

    # cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
    # cv2.resizeWindow("window", maxWidth, maxHeight)

    #print('About to show frame of Video.')
    cv2.imshow("Capturing", resized_image)
    #print('Running..')

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()