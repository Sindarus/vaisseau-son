#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-22

Reference for style conventions : https://www.python.org/dev/peps/pep-0008
"""

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QVBoxLayout, QGridLayout

from audio_player import AudioPlayer
from config import Config
from custom_style_groupbox import CustomStyleGroupBox
from image_option_button import ImageOptionButton


class SoundChooser(CustomStyleGroupBox):
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
        vertical_layout.addWidget(self.player)

        # Setup grid of sounds
        positions = [(i, j) for i in range(Config.SOUND_IMAGES_ROWS) for j in range(Config.SOUND_IMAGES_COLUMNS)]
        for pos, sound_button in zip(positions, self.sounds_buttons):
            sounds_buttons_layout.addWidget(sound_button, pos[0], pos[1], Qt.AlignCenter)

        self.selected_sound_name = self.sounds_buttons[0].get_name()
        self.player.load_sound(self.sound_bank[self.selected_sound_name]['sound_path'])

    def after_show_init(self):
        """Initializations that need to be done right after the mainwindow has been .show()'ed """
        # Selecting first sound at startup. We need to do that after the mainwindow has been .show()'n (and not before)
        # to avoid a display bug where the border of the sound_button widget would be taken into account to define its
        # size, which would make it bigger than the other buttons forever.
        self.sounds_buttons[0].setChecked(True)

    @pyqtSlot()
    def selected_sound_action(self):
        """Load sound into the player and update selected_sound_name.

        Is called when a sound gets selected."""
        sound_name = self.sender().get_name()  # get the name of the sound that was selected
        self.selected_sound_name = sound_name
        self.player.load_sound(self.sound_bank[self.selected_sound_name]['sound_path'], )

    def get_selected_sound_name(self):
        return self.selected_sound_name
