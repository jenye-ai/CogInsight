import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from ui_mainwindow import Ui_Form
from reports import Ui_Report

import cv2
import time
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from matplotlib import cm, gridspec
import numpy as np

import pyaudio
import constants
from pipeline import VideoPipeline
import wave
import soundfile as sf
import sounddevice as sd
import queue
import os
import time

class AudioRecorder(QThread):
    recording_finished = pyqtSignal()

    def __init__(self, samplerate=44100, filename=constants.ANSWER_PATH):
        super().__init__()
        self.fs = samplerate
        self.filename = filename
        self._stop = False
        self.duration = 0
        self.q = queue.Queue()

        # Get the names of the default input and output devices
        self.device = sd.default.device[0]
        device_info = sd.query_devices(self.device)
        self.channels = device_info['max_input_channels']

    def stop(self):
        self._stop = True

    def run(self):
        # Make sure the file is opened before recording anything:
        if os.path.exists(self.filename):
            os.remove(self.filename)
        with sf.SoundFile(self.filename, mode='x', samplerate=self.fs,
                        channels=self.channels) as file:
            with sd.InputStream(samplerate=self.fs, device=self.device,
                                channels=self.channels, callback=self.callback):
                while not self._stop:
                    file.write(self.q.get())

    def callback(self,indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        self.q.put(indata.copy())

    def stop(self):
        self._stop = True



class AudioPlayer(QThread):
    player_finished = pyqtSignal()

    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        wav_file = wave.open(constants.AUDIO_PATH, 'rb')
        # Get the sample rate and channels from the file
        sample_rate = wav_file.getframerate()
        channels = wav_file.getnchannels()

        # Create an instance of PyAudio
        self.audio = pyaudio.PyAudio()
        # Open a stream to play the audio
        self.stream = self.audio.open(format=self.audio.get_format_from_width(wav_file.getsampwidth()),
                            channels=channels,
                            rate=sample_rate,
                            output=True)

        # Read all the audio data and play it
        self.data = wav_file.readframes(wav_file.getnframes())

    def run(self):
        # Replace the file path with the path to your WAV file
        print("Player started!")
        self.stream.write(self.data)

        # Cleanup
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        self.player_finished.emit()

class MainWindow2(QMainWindow):
    # class constructor
    def __init__(self):
        # call QWidget constructor
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        navBar = self.create_navBar()

        mainLayout = QVBoxLayout()

        mainLayout.addWidget(navBar)
        mainLayout.setAlignment(Qt.AlignTop | Qt.AlignRight)

        self.ui.centralwidget.setLayout(mainLayout)

        self.ui.Transcript.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        # create a timer
        self.timer = QTimer()
        self.fps = 30

        self.video = cv2.VideoCapture(constants.QUESTION_PATH)
        self.video_fps = self.video.get(cv2.CAP_PROP_FPS)
        self.prev_index = 0
        #self.player = MediaPlayer(constants.ANSWER_PATH)

        self.timer.timeout.connect(self.viewCam)

        # set control_bt callback clicked  function
        self.ui.pushButton.clicked.connect(self.controlTimer)

        # initialize video writer
        self.video_writer = None

        # initialize audio recorder
        self.recorder = AudioRecorder()
        self.audio_player = AudioPlayer(constants.AUDIO_PATH)

        self.metrics = {}

        
    
    def viewCam(self):
        vret, vimage = self.video.read()
        if vret:
            height, width, channel = vimage.shape
            step = channel * width
            q_image = QImage(vimage.data, width, height, step, QImage.Format_BGR888)
            label_width = self.ui.Interviewer.width()
            label_height = self.ui.Interviewer.height()
            img_ratio = width / height
            label_ratio = label_width / label_height

            if img_ratio > label_ratio:
                # image is wider than label, scale by width
                scaled_width = label_width
                scaled_height = int(label_width / img_ratio)
            else:
                # image is taller than label, scale by height
                scaled_height = label_height
                scaled_width = int(label_height * img_ratio)
            q_image = q_image.scaled(scaled_width, scaled_height, Qt.KeepAspectRatio)
            # Display QImage on label
            pixmap = QPixmap.fromImage(q_image)
            self.ui.Interviewer.setPixmap(pixmap)

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

        label_width = self.ui.image_label.width()
        label_height = self.ui.image_label.height()
        img_ratio = width / height
        label_ratio = label_width / label_height

        if img_ratio > label_ratio:
            # image is wider than label, scale by width
            scaled_width = label_width
            scaled_height = int(label_width / img_ratio)
        else:
            # image is taller than label, scale by height
            scaled_height = label_height
            scaled_width = int(label_height * img_ratio)

        qImg = qImg.scaled(scaled_width, scaled_height, Qt.KeepAspectRatio)
        self.ui.image_label.setPixmap(QPixmap.fromImage(qImg))
        self.ui.image_label.setAlignment(Qt.AlignCenter)

        
        # write image to video
        if self.video_writer is not None:
            self.video_writer.write(cv2.cvtColor(image, cv2.COLOR_RGB2BGR))

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
            if constants.PC_TYPE == "Mac":
                self.cap = cv2.VideoCapture(0)
            else:
                self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            self.start_time = time.time()

            # initialize video writer
            if os.path.exists(constants.VIDEO_PATH):
                os.remove(constants.VIDEO_PATH)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.video_writer = cv2.VideoWriter(constants.VIDEO_PATH, fourcc, self.fps, (width, height))

            self.audio_player.start()
            
            self.recorder.start()
            self.ui.Transcript.setWordWrap(True)
            self.ui.Transcript.setText("TRANSCRIPT\n \nQ1: Hey, good to see you again! How have you been feeling?")
            

            # start timer
            self.timer.start(0)
            # update control_bt text
            self.ui.pushButton.setText("Done!")
        else:
            # stop timer
            self.timer.stop()
            # release video capture
            self.cap.release()

            # release video writer
            if self.video_writer is not None:
                self.video_writer.release()

            self.recorder.stop()

            self.audio_player.terminate()

            self.startLoadingScreen()

    def startLoadingScreen(self):
        # self.loading = LoadingScreen()
        # self.loading.metrics_done.connect(self.update_report)
        # self.setWindowTitle("Processing your video...")
        # self.loading.finished.connect(self.startReportScreen)
        # self.loading.show()
        self.loading = ReportScreen(self.metrics)
        self.loading.show()
        self.close()
        

    def startReportScreen(self):
        self.report = ReportScreen(self.metrics)
        self.report.show()
        self.close()

    def update_report(self, report_data):
        self.metrics = report_data

    def animate(self, start_rect, end_rect):
        self.setGeometry(*start_rect)
        self.show()
        
        animation = QPropertyAnimation(self, b"geometry")
        animation.setDuration(500)
        animation.setStartValue(QRect(*start_rect))
        animation.setEndValue(QRect(*end_rect))
        animation.start()

    def create_navBar(self):
        navBar = QWidget()
        navBarLayout = QHBoxLayout()
        
        aboutMenu = QPushButton("About")
        assessMenu = QPushButton("Assessment")
        resourceMenu = QPushButton("Resources")
        contactMenu = QPushButton("Contact Us")
        loginMenu = QPushButton("Login/Sign Up")
     
        navBarLayout.addWidget(aboutMenu)
        navBarLayout.addWidget(assessMenu)
        navBarLayout.addWidget(resourceMenu)
        navBarLayout.addWidget(contactMenu)
        navBarLayout.addWidget(loginMenu)
        navBarLayout.insertSpacing(0,400)
        
        navBar.setLayout(navBarLayout)
        
        return navBar

class ReportScreen(QMainWindow):
    # class constructor
    def __init__(self, metrics):
        # call QWidget constructor
        super().__init__()
        self.ui = Ui_Report()
        self.ui.setupUi(self)
        self.metrics = metrics
        self.ui.title.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        self.ui.b1.setValue(50)
        self.ui.b1.setStyleSheet('''
            QProgressBar {
                border-radius: 10px;
                text-align: right;
                color: red;
            }
            QProgressBar::chunk {
                background-color: pink;
                border-radius: 10px;
            }
        ''')  
        
        self.ui.b2.setValue(75)
        self.ui.b2.setStyleSheet('''
            QProgressBar {
                border-radius: 10px;
                text-align: right;
                color: red;
            }
            QProgressBar::chunk {
                background-color:#2c7EBC;
                border-radius: 10px;
            }
        ''')

        self.ui.b3.setValue(50)
        self.ui.b3.setStyleSheet('''
            QProgressBar {
                border-radius: 10px;
                text-align: right;
                color: green;
            }
            QProgressBar::chunk {
                background-color: purple;
                border-radius: 10px;
            }
        ''')
        
        self.ui.b4.setValue(20)
        self.ui.b4.setStyleSheet('''
            QProgressBar {
                border-radius: 10px;
                text-align: right;
                color: green;
            }
            QProgressBar::chunk {
                background-color: #57477D;
                border-radius: 10px;
            }
        ''')

class LoadingScreen(QWidget):
    metrics_done = pyqtSignal(object)
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.metrics = {}
        self.setWindowTitle("Processing Video ...")

        print('Thread is to be called here...')
        self.load()
        print('Thread has been called...')

        self.setWindowTitle("Results Finished! ...")
        self.metrics_done.emit(self.metrics)
        self.finished.emit()
        self.close()

    def load(self):
        # setup dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Processing Data ...")
        vbox = QVBoxLayout()
        lbl = QLabel(self)
        self.moviee = QMovie('loading.gif')
        lbl.setMovie(self.moviee)
        self.moviee.start()
        vbox.addWidget(lbl)
        dialog.setLayout(vbox)

        # setup thread
        thread = Worker()
        thread.report.connect(self.update_report)
        thread.finished.connect(thread.deleteLater)
        thread.finished.connect(dialog.close)
        thread.finished.connect(dialog.deleteLater)
        thread.start()

        dialog.exec()

    def update_report(self, report_data):
        self.metrics = report_data


    
        

class Worker(QThread):
    finished = pyqtSignal()
    report = pyqtSignal(object)

    def run(self):
        pipeline = VideoPipeline(constants.OUTPUT_DIR, frameRate=constants.FRAME_RATE, prefix = constants.IMAGE_PREFIX, folder = constants.FRAME_DIR, processed_folder = constants.PROCESSED_DIR)
        report = pipeline.execute(constants.VIDEO_PATH)
        self.report.emit(report)
        self.finished.emit()
        self.quit()
    
    def record_audio(self):
        pass
        


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create and show mainWindow
    mainWindow = MainWindow2()
    mainWindow.show()

    sys.exit(app.exec_())