#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-22

Reference for style conventions : https://www.python.org/dev/peps/pep-0008/#naming-conventions
"""

from PyQt5.QtCore import Qt, QUrl, pyqtSlot
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox

from Config import Config
from ImageButton import ImageButton
from ImageOptionButton import ImageOptionButton
from WaveformDisplay import WaveformDisplay


class SoundChooser(QGroupBox):
    """Widget that allows the user to choose a sound from a set, and to listen to it"""

    def __init__(self, parent_widget):
        super().__init__("Choisir un son", parent_widget)

        self.sound_bank = Config.SOUNDS

        self.init_ui()

    def init_ui(self):
        self.init_player()
        self.selected_sound_name = None  # name of the currently selected sound

        # Create widgets
        self.sounds_buttons = []
        for sound_name, sound in self.sound_bank.items():
            self.sounds_buttons.append(ImageOptionButton(sound['image_path'], sound_name))
            self.sounds_buttons[-1].resize_image(Config.SOUND_IMAGE_SIZE, Config.SOUND_IMAGE_SIZE)
            self.sounds_buttons[-1].clicked.connect(self.selected_sound_action)

        self.selected_sound_display = WaveformDisplay()
        self.selected_sound_play_button = ImageButton("images/play2.png")
        self.selected_sound_play_button.resize_image(Config.PLAYBACK_BUTTON_ICON_SIZE, Config.PLAYBACK_BUTTON_ICON_SIZE)
        self.selected_sound_play_button.clicked.connect(self.play_selected_sound)

        # Create layouts
        vertical_layout = QVBoxLayout()
        sounds_buttons_layout = QGridLayout()
        selected_sound_playback_layout = QHBoxLayout()

        # Setup vertical layout
        self.setLayout(vertical_layout)
        vertical_layout.addLayout(sounds_buttons_layout)
        vertical_layout.addStretch()
        vertical_layout.addLayout(selected_sound_playback_layout)

        # Setup grid of sounds
        positions = [(i, j) for i in range(Config.SOUND_IMAGES_ROWS) for j in range(Config.SOUND_IMAGES_COLUMNS)]
        for pos, sound_button in zip(positions, self.sounds_buttons):
            sounds_buttons_layout.addWidget(sound_button, pos[0], pos[1], Qt.AlignCenter)

        # Setup
        selected_sound_playback_layout.addWidget(self.selected_sound_play_button)
        selected_sound_playback_layout.addWidget(self.selected_sound_display)

        # Checking first button by default
        self.sounds_buttons[0].setChecked(True)
        self.selected_sound_name = self.sounds_buttons[0].get_name()
        self.update_waveform_display(self.selected_sound_name)

    def init_player(self):
        self.player = QSoundEffect()
        self.player.setVolume(1)
        self.player.playingChanged.connect(self.playing_changed_action)

    @pyqtSlot()
    def selected_sound_action(self):
        """Should get called when a sound gets selected"""
        sound_name = self.sender().get_name()  # get the name of the sound that was selected
        self.selected_sound_name = sound_name
        self.update_waveform_display(sound_name)

    def update_waveform_display(self, sound_name):
        sound_path = self.sound_bank[sound_name]['sound_path']
        self.selected_sound_display.load_audio(sound_path)

    @pyqtSlot()
    def play_selected_sound(self):
        self.selected_sound_play_button.setEnabled(False)

        sound_path = self.sound_bank[self.selected_sound_name]['sound_path']
        self.player.setSource(QUrl.fromLocalFile(sound_path))
        self.player.play()

    @pyqtSlot()
    def playing_changed_action(self):
        if not self.player.isPlaying():
            self.selected_sound_play_button.setEnabled(True)

    def report(self):
        print("Sound", self.selected_sound_name, "is selected")
