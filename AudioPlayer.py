#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-25

Reference for style conventions : https://www.python.org/dev/peps/pep-0008/#naming-conventions
"""
import wave

from PyQt5.QtCore import pyqtSlot, QUrl, QDateTime, QFile, QIODevice
from PyQt5.QtMultimedia import QSoundEffect, QAudioInput, QAudioFormat, QAudioDeviceInfo
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout

from Config import Config
from ImageButton import ImageButton
from WaveformDisplay import WaveformDisplay


class AudioPlayer(QWidget):

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
        self.play_button.setEnabled(True)

    def start_recording(self):
        print("recording")
        assert self.recordable
        datetime_stamp = QDateTime.currentDateTime().toString("yyyyMMdd_hhmmss")

        self.recorded_pcm_path = "user_sounds/user_sound_" + datetime_stamp + ".pcm"
        self.recorded_wav_path = "user_sounds/user_sound_" + datetime_stamp + ".wav"  # for use in stop_recording
        self.file_to_record.setFileName(self.recorded_pcm_path)
        self.file_to_record.open(QIODevice.WriteOnly | QIODevice.Truncate)

        self.recorder.start(self.file_to_record)

    def stop_recording(self):
        print("not recording")
        self.recorder.stop()
        self.file_to_record.close()

        self.pcm_to_wav(self.recorded_pcm_path, self.recorded_wav_path)
        self.load_sound(self.recorded_wav_path)
        if not self.is_recorded:
            self.is_recorded = True

    def get_recorded_sound_path(self):
        return self.recorded_wav_path

    @staticmethod
    def pcm_to_wav(pcm_input_file_path, wav_output_file_path):
        with open(pcm_input_file_path, 'rb') as pcmfile:
            pcmdata = pcmfile.read()
        with wave.open(wav_output_file_path, 'wb') as wavfile:
            wavfile.setparams((Config.N_CHANNELS,       # nchannels
                               Config.SAMPLE_SIZE/4,    # sampwidth (in bytes) (= sample size)
                               Config.SAMPLE_RATE,      # framerate (in hertz) (= sample rate)
                               0, "NONE", "NONE"))
            wavfile.writeframes(pcmdata)

    @pyqtSlot()
    def playing_changed_action(self):
        if not self.player.isPlaying():
            self.play_button.setEnabled(True)
