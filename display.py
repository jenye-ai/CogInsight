import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from ui_mainwindow import Ui_Form

import cv2
import time
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from matplotlib import cm, gridspec
import numpy as np
import collections
import pyaudio
import constants
from pipeline import VideoPipeline
import wave
import soundfile as sf
import sounddevice as sd
import queue
import os

class AudioRecorder(QThread):
    recording_finished = pyqtSignal()

    def __init__(self, samplerate=44100, filename=constants.ANSWER_PATH):
        super().__init__()
        self.fs = samplerate
        self.filename = filename
        self._stop = False
        self.duration = 0
        self.q = queue.Queue()
        # Get a list of available input devices
        #devices = sd.query_devices(kind='input')
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

    def run(self):
        # Replace the file path with the path to your WAV file
        print("Player started!")

        wav_file = wave.open(constants.AUDIO_PATH, 'rb')
        # Get the sample rate and channels from the file
        sample_rate = wav_file.getframerate()
        channels = wav_file.getnchannels()

        # Create an instance of PyAudio
        audio = pyaudio.PyAudio()
        # Open a stream to play the audio
        stream = audio.open(format=audio.get_format_from_width(wav_file.getsampwidth()),
                            channels=channels,
                            rate=sample_rate,
                            output=True)

        # Read all the audio data and play it
        data = wav_file.readframes(wav_file.getnframes())
        stream.write(data)

        # Cleanup
        stream.stop_stream()
        stream.close()
        audio.terminate()
        self.player_finished.emit()

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

        self.video = cv2.VideoCapture(constants.QUESTION_PATH)
        self.video_fps = self.video.get(cv2.CAP_PROP_FPS)
        self.prev_index = 0
        #self.player = MediaPlayer(constants.ANSWER_PATH)

        self.timer.timeout.connect(self.viewCam)

        # set control_bt callback clicked  function
        self.ui.pushButton.clicked.connect(self.controlTimer)

        # #Initialize audio player
        # channels, self.sample_rate, sample_width, self.wav_file = self.read_audio(constants.AUDIO_PATH)

        # # Set up audio player
        # self.audio_player = pyaudio.PyAudio()
        # self.audio_stream = self.audio_player.open(format=self.audio_player.get_format_from_width(sample_width), channels=channels, rate=self.sample_rate, output=True)
        
        # initialize video writer
        self.video_writer = None

        # initialize audio recorder
        self.recorder = AudioRecorder()
        self.audio_player = AudioPlayer(constants.AUDIO_PATH)
        # opening window in maximized size
        #self.showMaximized()
    
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
            filename, _ = QFileDialog.getSaveFileName(self, "Save video", ".", "MP4 files (*.mp4)")
            if filename:
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                self.video_writer = cv2.VideoWriter(filename, fourcc, self.fps, (width, height))

            #self.audio_recorder.record()
            self.recorder.start()
            self.audio_player.start()

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
            

            #self.wav_file.close()
            #self.audio_stream.close()
            self.audio_player.terminate()

            self.startLoadingScreen()


    def read_audio(self,file_path):
        # Open the audio file
        wf = wave.open(file_path, 'rb')

        # Get the audio file parameters
        channels = wf.getnchannels()
        sample_rate = wf.getframerate()
        sample_width = wf.getsampwidth()
        num_frames = wf.getnframes()
        audio_frames = wf.readframes(num_frames)
    
        self.audio_samples = int(num_frames / sample_rate * self.video_fps)
        return channels, sample_rate, sample_width, wf

    def startLoadingScreen(self):
        self.loading = LoadingScreen()
        self.setWindowTitle("Processing your video...")
        self.loading.show()

class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class LoadingScreen(QWidget):

    def __init__(self):
        super().__init__()
        self.metrics = {}
        self.setWindowTitle("Processing Video ...")

        print('Thread is to be called here...')
        self.load()
        print('Thread has been called...')

        self.figure = plt.figure()
  
        # this is the Canvas Widget that
        # displays the 'figure'it takes the
        # 'figure' instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
  
        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        #### PLOTTING DONE HERE #####
        # random data
        print(self.metrics)
        # clearing old figure
        self.figure.clear() 
        # create an axis
        a0 = self.figure.add_subplot(2,2,2)
        a1 = self.figure.add_subplot(2,2,4)
        a2 = self.figure.add_subplot(121, polar=True)

        #a0 is the number of smiles
        self.draw_bar(self.metrics["num_smiles"],self.metrics["num_smiles"]*2, a0)
        a0.set_title('Number of Smiles')
        #a1 is the time spent smiling
        self.draw_bar(self.metrics["time_smiling"],self.metrics["time"], a1)
        a1.set_title('Time Spent Smiling')
        #a2 is the radar plot
        self.draw_radar(self.metrics, a2)

        # refresh canvas
        self.canvas.draw()

        #####
  
        # creating a Vertical Box layout
        layout = QVBoxLayout()
          
        # adding tool bar to the layout
        layout.addWidget(self.toolbar)
          
        # adding canvas to the layout
        layout.addWidget(self.canvas)
          
          
        # setting layout to the main window
        self.setWindowTitle("Results")
        self.setLayout(layout)
  

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

    def draw_bar(self,level,max_level, ax):
        ax.bar([0], [max_level], width=1, edgecolor='black', fill=False)
        ax.bar([0], [level], width=1, color='blue')
        ax.set_xlim([0, max_level])
        ax.set_ylim([0, max_level])
        ax.tick_params(labelbottom=False)    
        ax.set_xticks([])
        return ax
    
    def draw_radar(self,report, ax):
        categories = ['neutral', 'happy','sad', 'surprise', 'fear', 'disgust', 'anger', 'contempt', 'none']
        categories = [*categories, categories[0]]
        count = collections.Counter(report["emotion"])
        for i in range(0,9):
            if i not in count.keys():
                count[i] = 0
        web = [count[i] for i in sorted(count.keys())]
        web = [*web, web[0]]

        label_loc = np.linspace(start=0, stop=2 * np.pi, num=len(web))

        ax.plot(label_loc, web, label='Emotions')
        ax.set_title('Distribution of emotions')
        ax.set_thetagrids(np.degrees(label_loc), labels=categories)

    
        

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
    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())