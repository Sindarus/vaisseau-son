#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-22

Reference for style conventions : https://www.python.org/dev/peps/pep-0008/#naming-conventions
"""

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QGroupBox

from AudioPlayer import AudioPlayer
from Config import Config
from ImageOptionButton import ImageOptionButton


class SoundChooser(QGroupBox):
    """Widget that allows the user to choose a sound from a set, and to listen to it"""

    def __init__(self, parent_widget):
        super().__init__("Choisir un son", parent_widget)

        self.sound_bank = Config.SOUNDS

        self.init_ui()

    def init_ui(self):
        self.selected_sound_name = None  # name of the currently selected sound

        # Create widgets
        self.sounds_buttons = []
        for sound_name, sound in self.sound_bank.items():
            self.sounds_buttons.append(ImageOptionButton(sound['image_path'], sound_name))
            self.sounds_buttons[-1].resize_image(Config.SOUND_IMAGE_SIZE, Config.SOUND_IMAGE_SIZE)
            self.sounds_buttons[-1].clicked.connect(self.selected_sound_action)
        self.player = AudioPlayer(False)

        # Create layouts
        vertical_layout = QVBoxLayout()
        sounds_buttons_layout = QGridLayout()

        # Setup vertical layout
        self.setLayout(vertical_layout)
        vertical_layout.addLayout(sounds_buttons_layout)
        vertical_layout.addStretch()
        vertical_layout.addWidget(self.player)

        # Setup grid of sounds
        positions = [(i, j) for i in range(Config.SOUND_IMAGES_ROWS) for j in range(Config.SOUND_IMAGES_COLUMNS)]
        for pos, sound_button in zip(positions, self.sounds_buttons):
            sounds_buttons_layout.addWidget(sound_button, pos[0], pos[1], Qt.AlignCenter)

        # Selecting first sound at startup
        self.sounds_buttons[0].setChecked(True)
        self.selected_sound_name = self.sounds_buttons[0].get_name()
        self.player.load_sound(self.sound_bank[self.selected_sound_name]['sound_path'])

    @pyqtSlot()
    def selected_sound_action(self):
        """Should get called when a sound gets selected"""
        sound_name = self.sender().get_name()  # get the name of the sound that was selected
        self.selected_sound_name = sound_name
        self.player.load_sound(self.sound_bank[self.selected_sound_name]['sound_path'])

    def report(self):
        print("Sound", self.selected_sound_name, "is selected")
