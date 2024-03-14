# Video Processor Application

The Video Processor application is a simple PyQt5-based tool for processing video streams. It allows users to open video files, display frames, apply image processing operations (such as thresholding), and save frames as image files.

## Features

- **Open Video File:** Load video files in formats such as `.mp4`, `.avi`, and `.mkv`.
- **Save Frame:** Save the current displayed frame as an image file in formats like `.png` and `.jpg`.
- **Start/Stop Video:** Begin and pause video playback.
- **Threshold Slider:** Adjust the threshold value applied to the video frames in real-time.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/suyyash10/Vyorius_test.git
    ```

2. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the application:

    ```bash
    python main.py
    ```

2. Open a video file using the "Open Video..." button or menu option.
3. Adjust the threshold slider to apply image processing operations (optional).
4. Click "Start" to begin video playback.
5. Click "Stop" to pause video playback.
6. Save frames using the "Save Frame..." button or menu option.
