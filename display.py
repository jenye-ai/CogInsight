import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from ui_mainwindow import Ui_Form

import cv2
import time

import constants
from pipeline import VideoPipeline
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

            self.startLoadingScreen()

    def startLoadingScreen(self):
        self.loading = LoadingScreen()
        self.setWindowTitle("Processing your video...")
        self.loading.show()

class LoadingScreen(QWidget):

    def __init__(self):
        super().__init__()

        print('Thread is to be called here...')
        self.load()
        print('Thread has been called...')

        # btn= QPushButton('Test button')
        # vbox = QVBoxLayout()
        # vbox.addWidget(btn)
        # self.setLayout(vbox)
        self.show()

    def load(self):
        # setup dialog
        dialog = QDialog(self)
        vbox = QVBoxLayout()
        lbl = QLabel(self)
        self.moviee = QMovie('loading.gif')
        lbl.setMovie(self.moviee)
        self.moviee.start()
        vbox.addWidget(lbl)
        dialog.setLayout(vbox)

        # setup thread
        thread = Worker()
        thread.finished.connect(thread.deleteLater)
        thread.finished.connect(dialog.close)
        thread.finished.connect(dialog.deleteLater)
        thread.start()

        dialog.exec()


class Worker(QThread):

    def run(self):
        pipeline = VideoPipeline(constants.OUTPUT_DIR, frameRate=constants.FRAME_RATE, prefix = constants.IMAGE_PREFIX, folder = constants.FRAME_DIR, processed_folder = constants.PROCESSED_DIR,)
        report = pipeline.execute(constants.VIDEO_PATH)
        print(report)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create and show mainWindow
    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())