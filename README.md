# Smart Parking Detection System

An automated computer vision project built with Python and OpenCV that monitors parking space availability in real time using video feeds.

## Features
- Interactive spot marker tool to select parking spaces using mouse clicks.
- Real-time video analysis to detect free and occupied parking spots.
- Automatic color-coded bounding boxes (Green for Available, Red for Occupied).
- Lightweight, free, and open-source with no extra hardware needed.

## Tech Stack
- Python
- OpenCV
- NumPy

## Project Files
- Picker.py: Interactive script to mark parking space coordinates.
- main.py: Main real-time computer vision detection script.
- parkingimg.jpg: Parking lot snapshot image.
- carPark.mp4: Live sample video feed.
- CarParkPos: Saved file containing parking spot coordinates.
- requirements.txt: List of required Python libraries.

## How to Run

1. Install requirements:
pip install -r requirements.txt

2. Run the space picker to mark parking spots:
python Picker.py
- Left click: Add parking box
- Right click: Delete parking box
- Press 'q': Save and exit

3. Run the live detection feed:
python main.py
- Press 'q': Exit video window
