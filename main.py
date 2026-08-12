import cv2
import pickle
import numpy as np

# Video feed
cap = cv2.VideoCapture('carPark.mp4')

# Bounding box dimensions (must match Picker.py)
width, height = 107, 48

# Load marked positions from Step 1
with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

def checkParkingSpace(imgPro, img):
    spaceCounter = 0

    for pos in posList:
        x, y = pos

        # Crop the image to the specific parking space region
        imgCrop = imgPro[y:y + height, x:x + width]
        
        # Count non-zero (white) pixels inside the cropped region
        count = cv2.countNonZero(imgCrop)

        # Threshold value: lower pixel count means the space is empty
        if count < 900:
            color = (0, 255, 0) # Green for Available
            thickness = 3
            spaceCounter += 1
        else:
            color = (0, 0, 255) # Red for Occupied
            thickness = 2

        # Draw the rectangle and pixel count overlay
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        cv2.putText(img, str(count), (x, y + height - 5), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)

    # Display total available parking spaces at the top-left
    cv2.rectangle(img, (40, 15), (420, 70), (0, 0, 0), cv2.FILLED)
    cv2.putText(img, f'Free Spots: {spaceCounter}/{len(posList)}', (50, 55),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

while True:
    # Loop the video continuously when it reaches the end
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()
    if not success:
        break

    # 1. Convert to Grayscale
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 2. Apply Gaussian Blur to reduce image noise
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    
    # 3. Adaptive Thresholding to convert to binary (black/white)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    
    # 4. Median Blur to remove isolated white noise pixels
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    
    # 5. Dilation to make edges thicker and easier to count
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    # Run the parking space evaluator
    checkParkingSpace(imgDilate, img)

    # Display the live detection window
    cv2.imshow("Smart Parking Detection", img)
    
    # Press 'q' to exit
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()