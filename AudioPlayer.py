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
from datetime import datetime

from PyQt5.QtCore import pyqtSlot, QUrl, QDateTime, QFile, QIODevice, pyqtSignal, QPropertyAnimation, QRect, QTimer
from PyQt5.QtMultimedia import QSoundEffect, QAudioInput, QAudioFormat, QAudioDeviceInfo, QAudio
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel

from Config import Config
from ImageButton import ImageButton
from WaveformDisplay import WaveformDisplay


class AudioPlayer(QWidget):
    """This class implements an audio reader and recorder."""

    was_recorded = pyqtSignal()
    """Signal that is emited when a sound was recorded"""
    recording_started = pyqtSignal(str, datetime)
    """Signal that is emited when the user just started recording"""

    def __init__(self, recordable=False):
        """*recordable* should be set to true if you want the :py:class:`AudioPlayer` to have recording abilities and a
        "rec" button. Recorded audio files will be stored in the *usersounds/* folder. If this folder does not exist,
        it is created.

        *self.sound_path* holds the path of the sound that is currently loaded in the player. *None* if no sound was
        loaded.
        """
        super().__init__()
        self.recordable = recordable
        self.sound_path = None
        self.recorded_datetime = None
        self.recorded_wav_path = None  # wav file
        self.recorded_pcm_path = None  # pcm file
        self.init_ui()
        self.init_player()
        self.is_recorded = False  # Set to true if a sound was recorded at least once
        self.is_currently_recording = False
        if recordable:
            self.init_recorder()
            # check output folder
            if not os.path.exists("user_sounds/"):
                os.makedirs("user_sounds/")

    def init_player(self):
        """Initialize the internal audio player"""
        self.player = QSoundEffect()
        self.player.setVolume(1)
        self.player.playingChanged.connect(self.playing_changed_action)

    def init_recorder(self):
        """Initialize the internal audio recorder"""
        self.file_to_record = QFile()

        audio_format = QAudioFormat()
        audio_format.setSampleRate(Config.SAMPLE_RATE)  # in hertz
        audio_format.setChannelCount(Config.N_CHANNELS)
        audio_format.setSampleSize(Config.SAMPLE_SIZE)  # in bits
        audio_format.setCodec("audio/pcm")
        audio_format.setByteOrder(QAudioFormat.LittleEndian)
        audio_format.setSampleType(QAudioFormat.SignedInt)

        # Selecting input device
        device_info = None
        for cur_device in QAudioDeviceInfo.availableDevices(QAudio.AudioInput):
            if "input" in cur_device.deviceName():
                device_info = cur_device
        if device_info is None:
            device_info = QAudioDeviceInfo.defaultInputDevice()
        print("Selecting input device", device_info.deviceName())

        if not device_info.isFormatSupported(audio_format):
            print("Default format not supported, trying to use the nearest. Supported formats:")
            print(device_info.supportedCodecs())
            audio_format = device_info.nearestFormat(audio_format)

        self.recorder = QAudioInput(device_info, audio_format)

    def init_ui(self):
        """Initialize child widgets and layout"""
        # Create widgets
        self.wave_display = WaveformDisplay()
        self.play_button = ImageButton("images/play2.png")
        self.play_button.resize_image(Config.PLAYBACK_BUTTON_ICON_SIZE, Config.PLAYBACK_BUTTON_ICON_SIZE)
        self.play_button.clicked.connect(self.play_sound)
        self.play_button.setEnabled(False)
        if self.recordable:
            self.rec_button = ImageButton("images/record.png")
            self.rec_button.resize_image(Config.PLAYBACK_BUTTON_ICON_SIZE, Config.PLAYBACK_BUTTON_ICON_SIZE)
            self.rec_button.clicked.connect(self.rec_button_clicked_action)

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
        """Start playing sound through the system's default output"""
        assert self.sound_path is not None, "Trying to play a sound but none were loaded in this AudioPlayer"

        self.cursor.pass_through()
        self.play_button.setEnabled(False)
        self.player.play()

    def load_sound(self, sound_path):
        """Load a sound into the player by passing its path"""
        self.sound_path = sound_path
        self.wave_display.load_audio(sound_path)
        self.player.setSource(QUrl.fromLocalFile(sound_path))

        # Handle cursor
        self.cursor.stop()
        self.cursor.set_duration(self.get_wav_duration(sound_path) * 1000)
        self.play_button.setEnabled(True)

    @pyqtSlot()
    def rec_button_clicked_action(self):
        """Handle what happens when the "rec" button is clicked"""
        if not self.is_currently_recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        """Start recording sound through the system's default microphone.

        Audio data is saved as a pcm (Pulse Code Modulation) file at first, using settings in :py:mod:`Config`.
        This function also handles changing the "rec" button into a "stop rec" button by changing its image."""
        print("recording")
        assert self.recordable

        self.reset()

        self.recorded_datetime = datetime.now()
        datetime_stamp = QDateTime.currentDateTime().toString("yyyyMMdd_hhmmss")
        self.recorded_pcm_path = "user_sounds/user_sound_" + datetime_stamp + ".pcm"
        self.recorded_wav_path = "user_sounds/user_sound_" + datetime_stamp + ".wav"  # for use in stop_recording
        self.file_to_record.setFileName(self.recorded_pcm_path)
        self.file_to_record.open(QIODevice.WriteOnly | QIODevice.Truncate)

        self.recorder.start(self.file_to_record)
        self.is_currently_recording = True
        self.rec_button.change_image("images/stop_record.png")

        self.recording_started.emit(self.recorded_wav_path, self.recorded_datetime)

        # In a while, check if the recording is not too long. The recording is identified by its pcm file saving
        # path, passed to the check-function. This argument HAS to be litteral : if we did use
        # self.recorded_pcm_path as argument, the check function would be called with the value of
        # self.recorded_pcm_path for the moment it is called, not the moment we define the timer.
        QTimer.singleShot(Config.AUDIO_RECORD_TIMOUT,
                          lambda: self.recording_timeout_check("user_sounds/user_sound_" + datetime_stamp + ".pcm"))

    def stop_recording(self):
        """Stop recording audio.

        The recorded audio PCM file is converted to WAV for use later on."""
        print("not recording")
        self.recorder.stop()
        self.file_to_record.close()

        self.pcm_to_wav(self.recorded_pcm_path, self.recorded_wav_path)
        self.load_sound(self.recorded_wav_path)
        if not self.is_recorded:
            self.is_recorded = True
            self.was_recorded.emit()

        self.is_currently_recording = False
        self.rec_button.change_image("images/record.png")

    def recording_timeout_check(self, specific_recorded_pcm_path):
        """Checks that the recording of file *specific_recorded_pcm_path* has ended. If not, then end it.

        This function is set (in :py:func:`start_recording`) to be called after Config.AUDIO_RECORD_TIMOUT ms,
        and is used to limit the maximum duration of a recording. First, we verify that the recording we're checking
        on hasn't ended and been replaced with a new one, then, if the recording is still ongoing, we stop it.
        """
        if self.recorded_pcm_path == specific_recorded_pcm_path:
            if self.is_currently_recording:
                self.stop_recording()

    def reset(self):
        """Reset the :py:class:`AudioPlayer` to the state it was when it was just created."""
        if self.is_currently_recording:
            self.stop_recording()

        self.sound_path = None
        self.recorded_datetime = None
        self.recorded_wav_path = None
        self.recorded_pcm_path = None
        self.is_recorded = False

        self.player.stop()
        self.play_button.setEnabled(False)

        self.wave_display.reset()

    def get_is_recorded(self):
        """Getter function for the *is_recorded* attribute"""
        return self.is_recorded

    def get_recorded_datetime(self):
        """Getter function for the *recorded_datetime* attribute"""
        return self.recorded_datetime

    def get_recorded_sound_path(self):
        """Getter function for the *recorded_wav_path* attribute"""
        return self.recorded_wav_path

    @pyqtSlot()
    def playing_changed_action(self):
        """handle what happens when the audio playback is finished playing."""
        if not self.player.isPlaying():
            self.play_button.setEnabled(True)
            self.cursor.stop()  # interrupt the cursor animation before its end, since the sound is finished playing

    @staticmethod
    def pcm_to_wav(pcm_input_file_path, wav_output_file_path):
        """Convert pcm file to wav file. PCM file settings are specified in the :py:mod:`Config` module."""
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
        """Get the duration a wav audio file."""
        with contextlib.closing(wave.open(wav_file_path, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
        return duration


class AudioCursor(QLabel):
    """Class meant to be used only by :py:class:`AudioPlayer` to implement a cursor that moves as the sound is being played.

    This is a QLabel whose size has been fixed to a thin vertical bar to look like a cursor. When initialized,
    you should specify its parent widget to be the :py:class:`WaveformDisplay` on which you want to display a cursor.
    That way, the cursor can position itself above the WaveformDisplay with the :py:func:`setGeometry` function. Call
    :py:func:`pass_through` to animate the cursor from the topleft position to the topright position. Internally,
    the mechanism of "property animation" of Qt is used to transfer the cursor from left to right. """

    def __init__(self, *args, **kwargs):
        """Initialize object"""
        super().__init__(*args, **kwargs)

        # config
        self.padding = 2  # equal to the border width of the waveform display, here
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
        """Set the animation duration to be *duration*. This has to be the duration of the audio file."""
        self.animation.setDuration(duration)

    def pass_through(self):
        """Launch the animation"""
        parent_size = self.parentWidget().size()
        self.animation.setEndValue(QRect(parent_size.width() - self.padding - self.width,
                                         self.padding,
                                         self.width, self.height))
        self.animation.start()

    def stop(self):
        """Interrupt the animation and put the cursor back to its topleft position"""
        self.animation.stop()
        self.setGeometry(self.default_geometry)
