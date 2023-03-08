import sys
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QWidget
from ui_mainwindow import Ui_Form
import cv2
import time

class MainWindow(QMainWindow):
    # class constructor
    def __init__(self):
        # call QWidget constructor
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # create a timer
        self.timer = QTimer()
        self.fps = 30
        # set timer timeout callback function
        self.timer.timeout.connect(self.viewCam)

        # set control_bt callback clicked  function
        self.ui.control_bt.clicked.connect(self.controlTimer)

        # initialize video writer
        self.video_writer = None

    # view camera
    def viewCam(self):
        # read image in BGR format
        ret, image = self.cap.read()
        # convert image to RGB format
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        # get image infos
        height, width, channel = image.shape
        step = channel * width
        # create QImage from image
        # cv2.imshow('dna', image)
        qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
        # show image in img_label
        self.ui.image_label.setPixmap(QPixmap.fromImage(qImg))

        # write image to video
        if self.video_writer is not None:
            self.video_writer.write(cv2.cvtColor(image, cv2.COLOR_RGB2BGR))

        #new code:
        # calculate elapsed time
        elapsed_time = time.time() - self.start_time
        # calculate delay time
        delay_time = max(1/self.fps - elapsed_time, 0)
        # restart timer with adjusted interval
        self.timer.start(int(delay_time * 1000))


    # start/stop timer
    def controlTimer(self):
        # if timer is stopped
        if not self.timer.isActive():
            # create video capture
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            self.start_time = time.time()

            # initialize video writer
            filename, _ = QFileDialog.getSaveFileName(self, "Save video", ".", "MP4 files (*.mp4)")
            if filename:
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                self.video_writer = cv2.VideoWriter(filename, fourcc, self.fps, (width, height))

            # start timer
            self.timer.start(0)
            # update control_bt text
            self.ui.control_bt.setText("Stop")
        else:
            # stop timer
            self.timer.stop()
            # release video capture
            self.cap.release()

            # release video writer
            if self.video_writer is not None:
                self.video_writer.release()

            # update control_bt text
            self.ui.control_bt.setText("Start")
            self.ui.image_label.setText("Camera")

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create and show mainWindow
    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())