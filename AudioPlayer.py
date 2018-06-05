#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-25

Reference for style conventions : https://www.python.org/dev/peps/pep-0008
"""

import contextlib
import os
import wave

from PyQt5.QtCore import pyqtSlot, QUrl, QDateTime, QFile, QIODevice, pyqtSignal, QPropertyAnimation, QRect
from PyQt5.QtMultimedia import QSoundEffect, QAudioInput, QAudioFormat, QAudioDeviceInfo
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel

from Config import Config
from ImageButton import ImageButton
from WaveformDisplay import WaveformDisplay


class AudioPlayer(QWidget):
    was_recorded = pyqtSignal()  # This signal is emited when a sound was recorded the first time
    recorded_too_short = pyqtSignal()  # This signal is emited when the user recorded a sound that was too short

    def __init__(self, recordable=False):
        super().__init__()
        self.recordable = recordable
        self.sound_path = None
        self.recorded_wav_path = None  # wav file
        self.recorded_pcm_path = None  # pcm file
        self.init_ui()
        self.init_player()
        self.is_recorded = False  # Set to true if a sound was recorded at least once
        if recordable:
            self.init_recorder()
            # check output folder
            if not os.path.exists("user_sounds/"):
                os.makedirs("user_sounds/")

    def init_player(self):
        self.player = QSoundEffect()
        self.player.setVolume(1)
        self.player.playingChanged.connect(self.playing_changed_action)

    def init_recorder(self):
        self.file_to_record = QFile()

        audio_format = QAudioFormat()
        audio_format.setSampleRate(Config.SAMPLE_RATE)  # in hertz
        audio_format.setChannelCount(Config.N_CHANNELS)
        audio_format.setSampleSize(Config.SAMPLE_SIZE)  # in bits
        audio_format.setCodec("audio/pcm")
        audio_format.setByteOrder(QAudioFormat.LittleEndian)
        audio_format.setSampleType(QAudioFormat.SignedInt)

        device_info = QAudioDeviceInfo.defaultInputDevice()
        if not device_info.isFormatSupported(audio_format):
            print("Default format not supported, trying to use the nearest. Supported formats:")
            print(device_info.supportedCodecs())
            audio_format = device_info.nearestFormat(audio_format)

        self.recorder = QAudioInput(device_info, audio_format)

    def init_ui(self):
        # Create widgets
        self.wave_display = WaveformDisplay()
        self.play_button = ImageButton("images/play2.png")
        self.play_button.resize_image(Config.PLAYBACK_BUTTON_ICON_SIZE, Config.PLAYBACK_BUTTON_ICON_SIZE)
        self.play_button.clicked.connect(self.play_sound)
        self.play_button.setEnabled(False)
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

        # Setup plaback cursor
        self.cursor = AudioCursor(self.wave_display)

    @pyqtSlot()
    def play_sound(self):
        assert self.sound_path is not None, "Trying to play a sound but none were loaded in this AudioPlayer"

        self.cursor.pass_through()
        self.play_button.setEnabled(False)
        self.player.play()

    def load_sound(self, sound_path):
        self.sound_path = sound_path
        self.wave_display.load_audio(sound_path)
        self.player.setSource(QUrl.fromLocalFile(sound_path))

        # Handle cursor
        self.cursor.stop()
        self.cursor.set_duration(self.get_wav_duration(sound_path) * 1000)
        self.play_button.setEnabled(True)

    @pyqtSlot()
    def start_recording(self):
        # TODO: faire clignoter quelque-chose pendant l'enregistrement
        print("recording")
        assert self.recordable
        datetime_stamp = QDateTime.currentDateTime().toString("yyyyMMdd_hhmmss")

        self.recorded_pcm_path = "user_sounds/user_sound_" + datetime_stamp + ".pcm"
        self.recorded_wav_path = "user_sounds/user_sound_" + datetime_stamp + ".wav"  # for use in stop_recording
        self.file_to_record.setFileName(self.recorded_pcm_path)
        self.file_to_record.open(QIODevice.WriteOnly | QIODevice.Truncate)

        self.recorder.start(self.file_to_record)

    @pyqtSlot()
    def stop_recording(self):
        print("not recording")
        self.recorder.stop()
        self.file_to_record.close()

        self.pcm_to_wav(self.recorded_pcm_path, self.recorded_wav_path)
        if self.get_wav_duration(self.recorded_wav_path) < 0.5:
            self.wave_display.reset()
            self.reset()
            self.recorded_too_short.emit()
            return

        self.load_sound(self.recorded_wav_path)
        if not self.is_recorded:
            self.is_recorded = True
            self.was_recorded.emit()

    def reset(self):
        self.sound_path = None
        self.recorded_wav_path = None
        self.recorded_pcm_path = None
        self.is_recorded = False

        self.player.stop()
        self.play_button.setEnabled(True)

        self.wave_display.reset()

    def get_recorded_sound_path(self):
        return self.recorded_wav_path

    @pyqtSlot()
    def playing_changed_action(self):
        if not self.player.isPlaying():
            self.play_button.setEnabled(True)
            self.cursor.stop()  # interrupt the cursor animation before its end, since the sound is finished playing

    @staticmethod
    def pcm_to_wav(pcm_input_file_path, wav_output_file_path):
        with open(pcm_input_file_path, 'rb') as pcmfile:
            pcmdata = pcmfile.read()
        with wave.open(wav_output_file_path, 'wb') as wavfile:
            wavfile.setparams((Config.N_CHANNELS,  # nchannels
                               Config.SAMPLE_SIZE // 8,  # sampwidth (in bytes) (= sample size)
                               Config.SAMPLE_RATE,  # framerate (in hertz) (= sample rate)
                               0, "NONE", "NONE"))
            wavfile.writeframes(pcmdata)

    @staticmethod
    def get_wav_duration(wav_file_path):
        with contextlib.closing(wave.open(wav_file_path, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
        return duration


class AudioCursor(QLabel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # config
        self.padding = 2    # equal to the border width of the waveform display, here
        self.width = 4
        self.height = Config.WAVEFORM_DISPLAY_HEIGHT - 2 * 2

        self.default_geometry = QRect(self.padding, self.padding, self.width, self.height)
        self.setFixedSize(self.width, self.height)
        self.setGeometry(self.default_geometry)
        self.setStyleSheet("""
            AudioCursor {
                background-color: green;
            }
        """)

        # Setup animation
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setStartValue(self.default_geometry)
        self.animation.finished.connect(lambda: self.setGeometry(self.default_geometry))

    def set_duration(self, duration):
        self.animation.setDuration(duration)

    def pass_through(self):
        parent_size = self.parentWidget().size()
        self.animation.setEndValue(QRect(parent_size.width()-self.padding-self.width,
                                         self.padding,
                                         self.width,  self.height))
        self.animation.start()

    def stop(self):
        self.setGeometry(self.default_geometry)
        self.animation.stop()
