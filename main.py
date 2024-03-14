import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QSlider, QAction, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from functools import partial

class VideoProcessor(QMainWindow):
    def __init__(self):
        super().__init__()

        # Default video source (webcam)
        self.video_source = 0  

        # Open video capture
        self.cap = cv2.VideoCapture(self.video_source)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Create central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Video display label
        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignCenter)

        # Start and stop buttons
        self.start_button = QPushButton('Start')
        self.start_button.clicked.connect(self.start_video)

        self.stop_button = QPushButton('Stop')
        self.stop_button.clicked.connect(self.stop_video)
        self.stop_button.setEnabled(False)

        # Threshold slider
        self.threshold_slider = QSlider(Qt.Horizontal)
        self.threshold_slider.setMinimum(0)
        self.threshold_slider.setMaximum(255)
        self.threshold_slider.setValue(127)
        self.threshold_slider.valueChanged.connect(self.update_threshold)

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.threshold_slider)

        self.central_widget.setLayout(layout)

        # Timer for video update
        self.timer = None

        # Create actions for menu
        self.create_actions()

        # Create toolbar
        self.create_toolbar()

    def create_actions(self):
        # Action to open video file
        self.open_action = QAction("&Open Video...", self)
        self.open_action.triggered.connect(self.open_video_file)

        # Action to save frame
        self.save_action = QAction("&Save Frame...", self)
        self.save_action.triggered.connect(self.save_frame)

    def create_toolbar(self):
        # Create toolbar for menu actions
        toolbar = self.addToolBar("Tools")
        toolbar.addAction(self.open_action)
        toolbar.addAction(self.save_action)

    def open_video_file(self):
        # Open a video file using a file dialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Video File", "", "Video Files (*.mp4 *.avi *.mkv)")
        if file_name:
            self.cap.release()  # Release previous video capture
            self.cap = cv2.VideoCapture(file_name)  # Open new video file

    def save_frame(self):
        # Save the current displayed frame as an image file
        if self.video_label.pixmap():
            file_name, _ = QFileDialog.getSaveFileName(self, "Save Frame", "", "Images (*.png *.jpg)")
            if file_name:
                self.video_label.pixmap().save(file_name)

    def start_video(self):
        # Start displaying video frames
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.timer = self.startTimer(30)  # Update every 30 milliseconds

    def stop_video(self):
        # Stop displaying video frames
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        if self.timer is not None:
            self.killTimer(self.timer)
            self.timer = None

    def timerEvent(self, event):
        # Event triggered for timer, reads frame and updates display
        ret, frame = self.cap.read()
        if ret:
            processed_frame = self.process_frame(frame)
            self.display_frame(processed_frame)

    def process_frame(self, frame):
        # Process frame (example: convert to grayscale and apply threshold)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresholded_frame = cv2.threshold(gray_frame, self.threshold_slider.value(), 255, cv2.THRESH_BINARY)
        return thresholded_frame

    def display_frame(self, frame):
        # Display frame on QLabel
        h, w = frame.shape
        q_img = QImage(frame.data, w, h, w, QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(q_img)
        self.video_label.setPixmap(pixmap)

    def update_threshold(self, value):
        # Placeholder function for updating threshold value
        pass  

    def closeEvent(self, event):
        # Release video capture when closing the application
        self.cap.release()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VideoProcessor()
    window.setWindowTitle('Video Processor')
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())
