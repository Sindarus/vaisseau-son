#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-22

Reference for style conventions : https://www.python.org/dev/peps/pep-0008/#naming-conventions
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox

from ImageOptionButton import ImageOptionButton
from ImageOptionButtonGroup import ImageOptionButtonGroup
from WaveformDisplay import WaveformDisplay


class SoundChooser(QGroupBox):
    """Widget that allows the user to choose a sound from a set, and to listen to it"""

    def __init__(self, parent_widget):
        super().__init__("Choisir un son", parent_widget)
        self.init_ui()

    def init_ui(self):
        # Create a group for sound selector buttons
        self.sound_button_group = ImageOptionButtonGroup()

        # Create widgets
        # TODO: add different sounds/images
        sounds_buttons = [ImageOptionButton("images/test.jpg") for i in range(8)]
        for sound_button in sounds_buttons:
            sound_button.resize_image(150, 150)
            self.sound_button_group.add_image_button(sound_button)
        selected_sound_display = WaveformDisplay()
        selected_sound_display.load_audio("212764__qubodup__lion-roar.flac")
        selected_sound_play_button = ImageOptionButton("images/play2.png")
        selected_sound_play_button.resize_image(100, 100)

        # Create layouts
        vertical_layout = QVBoxLayout()
        sounds_buttons_layout = QGridLayout()
        selected_sound_playback_layout = QHBoxLayout()

        # Setup vertical layout
        self.setLayout(vertical_layout)
        vertical_layout.addLayout(sounds_buttons_layout)
        vertical_layout.addLayout(selected_sound_playback_layout)

        # Setup grid of sounds
        positions = [(i, j) for i in range(2) for j in range(4)]
        for pos, sound_button in zip(positions, sounds_buttons):
            sounds_buttons_layout.addWidget(sound_button, pos[0], pos[1], Qt.AlignCenter)

        # Setup
        selected_sound_playback_layout.addWidget(selected_sound_play_button)
        selected_sound_playback_layout.addWidget(selected_sound_display)

    def report(self):
        self.sound_button_group.report()
