# EEG-signal-simulator
# EEG Signal Simulator with Real-Time Sound Feedback

This Python project simulates an EEG (Electroencephalogram) signal in real-time, displays the waveform, and plays different sounds based on signal frequency and spike detection.

## 🚀 Features
- Real-time EEG signal plotting with adjustable frequency and noise
- Spike detection with sound alerts using pygame
- Interactive control using OpenCV trackbars
- Save EEG plot snapshot with a key press

## 📦 Requirements
- Python 3.x
- OpenCV
- Matplotlib
- NumPy
- Pygame

## 🔊 Sound Alerts
- **Low frequency** (< 7 Hz): low_beep.wav
- **Mid frequency** (7–15 Hz): mid_beep.wav
- **High frequency** (> 15 Hz): high_beep.wav

## 🖥️ How to Run
1. Install the requirements:
   ```bash
   pip install opencv-python matplotlib numpy pygame
