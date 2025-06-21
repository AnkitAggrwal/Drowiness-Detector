# Drowiness-Detector

This project implements a real-time driver drowsiness detection system using Python, OpenCV, and Mediapipe. It monitors the driver's eye aspect ratio to detect signs of drowsiness or fatigue and plays an alarm sound when drowsiness is detected.

## 🚗 Features

- Real-time video feed from webcam
- Eye detection using Mediapipe's Face Mesh
- Eye Aspect Ratio (EAR) calculation
- Audio alarm when eyes are closed beyond a threshold
- Lightweight and works in real time on CPU

## 🛠️ Technologies Used

- Python 3.10+
- OpenCV
- Mediapipe (for face and eye landmark detection)
- Pygame (for playing the alarm sound)

## 📦 Installation

Install the required packages using:

```bash
pip install opencv-python mediapipe pygame

▶️ How to Run
Run the script with:

python main.py

Make sure your webcam is connected and working. The script will monitor your eyes and play an alert if it detects signs of drowsiness.

📁 Project Structure
DROWINESS DETECTOR/
├── venv/
├── alarm-301729.wav
├── main.py

📊 How It Works
Mediapipe Face Mesh detects facial landmarks including eyes.

Calculates Eye Aspect Ratio (EAR) to determine whether the eyes are closed.

If the eyes stay closed for a threshold number of frames, it triggers an audio alert using pygame.


