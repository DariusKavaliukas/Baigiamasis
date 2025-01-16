import sys
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout,
                             QSlider, QStyle, QFileDialog)

file_types = "*.mp3 *.mp4 *.wmv *.avi *.mkv"


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QTCinema")
        self.setGeometry(650, 400, 1280, 720)
        self.setWindowIcon(QIcon('cinema_icon.png'))
        colour = self.palette()
        colour.setColor(QPalette.Window, Qt.black)
        self.setPalette(colour)

        self.player_ui()
        self.show()

    def player_ui(self):
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        video_widget = QVideoWidget()

        open_button = QPushButton('Open')
        open_button.clicked.connect(self.open_file)

        self.play_button = QPushButton()
        self.play_button.setEnabled(False)
        self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_button.clicked.connect(self.play_video)

        self.video_slider = QSlider(Qt.Horizontal)
        self.video_slider.setRange(0, 0)
        self.video_slider.sliderMoved.connect(self.set_position)

        self.fullscreen_button = QPushButton()
        self.fullscreen_button.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        self.fullscreen_button.clicked.connect(self.fullscreen_control)

        self.volume_slider = QSlider(Qt.Vertical)
        self.volume_slider.setFixedHeight(50)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(75)
        self.volume_slider.sliderMoved.connect(self.volume_control)

        horizontal_layout = QHBoxLayout()
        horizontal_layout.setContentsMargins(0, 0, 0, 0)
        horizontal_layout.addWidget(open_button)
        horizontal_layout.addWidget(self.play_button)
        horizontal_layout.addWidget(self.video_slider)
        horizontal_layout.addWidget(self.fullscreen_button)
        horizontal_layout.addWidget(self.volume_slider)

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(video_widget)
        vertical_layout.addLayout(horizontal_layout)

        self.setLayout(vertical_layout)
        self.media_player.setVideoOutput(video_widget)

        self.media_player.stateChanged.connect(self.mediastate_changed)
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Video", filter=file_types)

        if file_name != '':
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(file_name)))
            self.play_button.setEnabled(True)

    def play_video(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()

    def mediastate_changed(self, state):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def position_changed(self, position):
        self.video_slider.setValue(position)

    def duration_changed(self, duration):
        self.video_slider.setRange(0, duration)

    def set_position(self, position):
        self.media_player.setPosition(position)

    def fullscreen_control(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def volume_control(self, volume):
        self.media_player.setVolume(volume)


app = QApplication(sys.argv)
window = Window()
app.exec()
