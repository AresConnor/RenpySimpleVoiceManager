from PySide6 import QtGui
from PySide6.QtCore import QUrl, QTimer
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput, QMediaFormat
from PySide6.QtWidgets import QDialog

from .ui.audioPlayerUI import AudioPlayerUI


def showDurationTime(duration: int):
    """
    Convert duration to time string and show
    like xx:xx
    """
    duration = duration / 1000
    minutes = int(duration / 60)
    seconds = int(duration % 60)
    return f"{minutes:02d}:{seconds:02d}"


def getSupportAudioFormat1():
    supportMimeType = set()
    for fileFormat in QMediaFormat().supportedFileFormats(QMediaFormat.ConversionMode.Decode):
        supportMimeType.update(QMediaFormat(fileFormat).mimeType().suffixes())
    supportMimeType.add("wav")
    supportMimeType = tuple(supportMimeType)
    return supportMimeType


def getSupportAudioFormat():
    rv = ("wav", "mp3", "m4a", "flac", "aac", "wma")
    return rv


class AudioPlayerDialog(QDialog):
    def __init__(self, title, audioFile, parent=None):
        super().__init__(parent)

        # Load the UI file
        self.updateSliderPosition = None
        self.audio_file = audioFile
        self.ui = AudioPlayerUI()
        self.ui.setupUi(self)
        self.ui.audioPosSlider.setTickInterval(0)
        self.ui.audioPosSlider.setPageStep(0)
        self.ui.volumeSlider.setMaximum(100)

        # Set the window title
        self.setWindowTitle(title)

        # Create a media player and output
        self.mediaPlayer = QMediaPlayer(self)
        self.audioOutput = QAudioOutput()
        self.audioOutput.setVolume(0.5)

        # debug
        self.mediaPlayer.errorOccurred.connect(lambda e, m: print(self.__class__.__name__, e, m))

        # Set the audio output
        self.mediaPlayer.setAudioOutput(self.audioOutput)

        # read audio file
        self.mediaPlayer.setSource(QUrl.fromLocalFile(audioFile))

        # link the buttons to the media player
        self.ui.playBtn.clicked.connect(self.mediaPlayer.play)
        self.ui.pauseBtn.clicked.connect(self.mediaPlayer.pause)

        # show audio duration
        self.mediaPlayer.durationChanged.connect(lambda ms: {
            self.ui.audioDuration.setText(showDurationTime(ms)),
            self.ui.audioPosSlider.setRange(0, ms)
        })
        self.mediaPlayer.positionChanged.connect(self.onMediaPlayerPosChanged)

        # setting up timer
        self.timer = QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.updateSlider)

        # apply audio position slider
        self.ui.audioPosSlider.sliderMoved.connect(self.onSliderMoved)
        self.ui.audioPosSlider.sliderPressed.connect(self.mediaPlayer.pause)
        self.ui.audioPosSlider.sliderReleased.connect(self.mediaPlayer.play)

        # set audio volume slider value before connecting
        self.ui.volumeSlider.setValue(50)

        # apply relative value in audio volume slider to audio output
        self.ui.volumeSlider.valueChanged.connect(lambda v: {
            self.audioOutput.setVolume(v / 100),
            self.ui.currentVolume.setText(f"{v}%".rjust(4, " "))
        })

        self.mediaPlayer.play()

    def onSliderMoved(self, value):
        self.mediaPlayer.setPosition(value)

    def onMediaPlayerPosChanged(self, ms):
        self.ui.currentAudioPos.setText(showDurationTime(ms))

        self.updateSliderPosition = True
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateSlider)
        self.timer.start(100)

    def updateSlider(self):
        if self.mediaPlayer.mediaStatus() == QMediaPlayer.MediaStatus.BufferedMedia:
            self.timer.start()
            self.ui.audioPosSlider.setValue(self.mediaPlayer.position())
        else:
            self.timer.stop()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.mediaPlayer.stop()
        self.mediaPlayer.setSource(QUrl())
        self.mediaPlayer.disconnect()
        super().closeEvent(a0)
