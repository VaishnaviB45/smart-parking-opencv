import cv2
import pickle

# Width and Height of a single parking space box
width, height = 107, 48

# Load existing positions if available, otherwise start with an empty list
try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []

def mouseClick(events, x, y, flags, params):
    # Left click to ADD a parking spot
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    # Right click to REMOVE a parking spot
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)

    # Save updated positions to a file
    with open('CarParkPos', 'wb') as f:
        pickle.dump(posList, f)

while True:
    img = cv2.imread('parkingimg.png') # Replace with your image file name
    
    # Draw boxes for all saved parking positions
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

    cv2.imshow("Parking Space Picker", img)
    cv2.setMouseCallback("Parking Space Picker", mouseClick)
    
    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()