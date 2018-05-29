#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-25

Reference for style conventions : https://www.python.org/dev/peps/pep-0008/#naming-conventions
"""
from PyQt5.QtCore import pyqtSlot, QUrl, QDateTime
from PyQt5.QtMultimedia import QSoundEffect, QAudioRecorder, QAudioEncoderSettings, QMultimedia, QMediaRecorder
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout

from Config import Config
from ImageButton import ImageButton
from WaveformDisplay import WaveformDisplay


class AudioPlayer(QWidget):

    def __init__(self, recordable=False):
        super().__init__()
        self.recordable = recordable
        self.sound_path = None
        self.init_ui()
        self.init_player()
        if recordable:
            self.init_recorder()

    def init_player(self):
        self.player = QSoundEffect()
        self.player.setVolume(1)
        self.player.playingChanged.connect(self.playing_changed_action)

    def init_recorder(self):
        self.recorder = QAudioRecorder()
        audio_settings = QAudioEncoderSettings()
        audio_settings.setCodec("audio/wav")
        audio_settings.setQuality(QMultimedia.HighQuality)
        self.recorder.setEncodingSettings(audio_settings)

    def init_ui(self):
        # Create widgets
        self.wave_display = WaveformDisplay()
        self.play_button = ImageButton("images/play2.png")
        self.play_button.resize_image(Config.PLAYBACK_BUTTON_ICON_SIZE, Config.PLAYBACK_BUTTON_ICON_SIZE)
        self.play_button.clicked.connect(self.play_sound)
        if self.recordable:
            self.rec_button = ImageButton("images/record.png")
            self.rec_button.resize_image(Config.PLAYBACK_BUTTON_ICON_SIZE, Config.PLAYBACK_BUTTON_ICON_SIZE)
            self.rec_button.pressed.connect(self.start_recording)
            self.rec_button.released.connect(self.stop_recording)

        # Setup layout for play and rec buttons
        self.buttons_layout = QVBoxLayout()
        self.buttons_layout.addWidget(self.play_button)
        if self.recordable:
            self.buttons_layout.addWidget(self.rec_button)

        # Setup main layout
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.addLayout(self.buttons_layout)
        self.main_layout.addWidget(self.wave_display)

        self.setStyleSheet("""
            QFrame, QLabel, QToolTip {
                border: 5px solid green;
            }
            """)

    def play_sound(self):
        assert self.sound_path is not None, "Trying to play a sound but none were loaded in this AudioPlayer"

        self.play_button.setEnabled(False)
        self.player.play()

    def load_sound(self, sound_path):
        self.sound_path = sound_path
        self.wave_display.load_audio(sound_path)
        self.player.setSource(QUrl.fromLocalFile(sound_path))

    def start_recording(self):
        print("recording")
        assert self.recordable
        datetime_stamp = QDateTime.currentDateTime().toString("yyyyMMdd_hhmmss")
        self.recorder.setOutputLocation(QUrl.fromLocalFile("user_sounds/user_sound_" + datetime_stamp + ".wav"))
        assert self.recorder.status() == QMediaRecorder.LoadedStatus, \
            "Media Recorder not ready to record. Status :" + str(self.recorder.status())
        self.recorder.record()

    def stop_recording(self):
        print("not recording")
        self.recorder.stop()

    @pyqtSlot()
    def playing_changed_action(self):
        if not self.player.isPlaying():
            self.play_button.setEnabled(True)
