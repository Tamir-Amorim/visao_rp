import sys
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit, QLabel
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtGui import QImage, QPixmap
from simple_facerec import SimpleFacerec
import os


sfr = SimpleFacerec()
sfr.load_encoding_images("images/**")

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Face Recognition Software'
        self.left = 10
        self.top = 10
        self.width = 1000
        self.height = 600
        self.frame_counter = 0  # Initialize frame counter
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        # Main layout
        main_layout = QVBoxLayout()

        # Camera label
        self.camera_label = QLabel(self)
        main_layout.addWidget(self.camera_label)

        # Name input
        self.name_input = QLineEdit(self)
        main_layout.addWidget(self.name_input)

        # Buttons layout
        buttons_layout = QHBoxLayout()

        # Capture button
        self.capture_button = QPushButton('Capture', self)
        self.capture_button.clicked.connect(self.on_capture_click)
        buttons_layout.addWidget(self.capture_button)

        # Retrain button
        self.retrain_button = QPushButton('Retrain', self)
        self.retrain_button.clicked.connect(self.on_retrain_click)
        buttons_layout.addWidget(self.retrain_button)

        # Add buttons layout to main layout
        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

        # Camera setup
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1000.0/30)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Flip the frame horizontally (mirror effect)
            frame = cv2.flip(frame, 1)

            # Resize the image to fit the window
            self.frame_counter += 1
            if self.frame_counter % 10 == 5:
                # Perform your operation here
                self.face_locations, self.face_names = sfr.detect_known_faces(frame)
            for face_loc, name in zip(self.face_locations, self.face_names):
                y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
                #print(face_loc)

                cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)
            frame = cv2.resize(frame, (self.width, int(self.width * frame.shape[0] / frame.shape[1])))
            image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888).rgbSwapped()
            self.camera_label.setPixmap(QPixmap.fromImage(image))

            # Increment frame counter and check if it's time to perform an operation

    @pyqtSlot()
    def on_capture_click(self):
        name = self.name_input.text()
        ret, frame = self.cap.read()
        if ret:
            # Here you can add code to process and save the frame with the associated name
            path = f"./images/{name}"
            if not os.path.exists(path):
                os.mkdir(path)
            picnumber = len(os.listdir(path))
            cv2.imwrite(f'{path}/{picnumber}.png', frame)

    @pyqtSlot()
    def on_retrain_click(self):
        # Add code for the retraining process here
        sfr.load_encoding_images("images/**")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
