import numpy as np
import cv2

def nothing(x):
    pass

print('Version: ' + cv2.__version__)

cap = cv2.VideoCapture(0)

# Setup Window
cv2.namedWindow('Image')
cv2.createTrackbar('R Low', 'Image', 0, 255, nothing)
cv2.createTrackbar('G Low', 'Image', 0, 255, nothing)
cv2.createTrackbar('B Low', 'Image', 0, 255, nothing)
cv2.createTrackbar('R High', 'Image', 0, 255, nothing)
cv2.createTrackbar('G High', 'Image', 0, 255, nothing)
cv2.createTrackbar('B High', 'Image', 0, 255, nothing)

while(True):
    ret, frame = cap.read()

    # Get RGB Values
    rLow = cv2.getTrackbarPos('R Low', 'Image')
    gLow = cv2.getTrackbarPos('G Low', 'Image')
    bLow = cv2.getTrackbarPos('B Low', 'Image')
    rHigh = cv2.getTrackbarPos('R High', 'Image')
    gHigh = cv2.getTrackbarPos('G High', 'Image')
    bHigh = cv2.getTrackbarPos('B High', 'Image')

    # Threshold image
    rgbLows = np.array([bLow, gLow, rLow],dtype= np.uint8)
    rgbHighs = np.array([bHigh, gHigh, rHigh], dtype=np.uint8)

    # Get Mask
    mask = cv2.inRange(frame, rgbLows, rgbHighs)

    # Get Contours
    im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE,
                                                cv2.CHAIN_APPROX_SIMPLE)

    # draw the contours
    cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)

    # Show final image
    cv2.imshow('Image', mask)
    cv2.imshow('Raw Image', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
