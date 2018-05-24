#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-22

Reference for style conventions : https://www.python.org/dev/peps/pep-0008/#naming-conventions
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox

from ImageButton import ImageButton
from ImageOptionButton import ImageOptionButton
from ImageOptionButtonGroup import ImageOptionButtonGroup
from WaveformDisplay import WaveformDisplay


class SoundChooser(QGroupBox):
    """Widget that allows the user to choose a sound from a set, and to listen to it"""

    def __init__(self, parent_widget):
        super().__init__("Choisir un son", parent_widget)

        self.sound_bank = []  # list of dict containing the path to the sound and the path to the image
        self.sound_bank.append({'sound_path': "sounds/232289__zglar__zombie-or-monster-or-lion-roar.wav",
                                'image_path': "images/lion.png"})
        self.sound_bank.append({'sound_path': "sounds/58277__benboncan__cow.wav",
                                'image_path': "images/cow.png"})
        self.sound_bank.append({'sound_path': "sounds/90014__thfc140491__police-siren-perpignan_cropped.wav",
                                'image_path': "images/police.png"})
        self.sound_bank.append({'sound_path': "sounds/84111__benboncan__wind-on-door-short_cropped.wav",
                                'image_path': "images/wind.png"})

        self.init_ui()

    def init_ui(self):
        # Create a group for sound selector buttons
        self.sound_button_group = ImageOptionButtonGroup()

        # Create widgets
        sounds_buttons = []
        for sound in self.sound_bank:
            img_opt_button = ImageOptionButton(sound['image_path'])
            img_opt_button.resize_image(150, 150)
            self.sound_button_group.add_image_button(img_opt_button)
            sounds_buttons.append(img_opt_button)

        selected_sound_display = WaveformDisplay()
        selected_sound_display.load_audio("sounds/232289__zglar__zombie-or-monster-or-lion-roar.wav")
        selected_sound_play_button = ImageButton("images/play2.png")
        selected_sound_play_button.resize_image(100, 100)

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
        positions = [(i, j) for i in range(1) for j in range(4)]
        for pos, sound_button in zip(positions, sounds_buttons):
            sounds_buttons_layout.addWidget(sound_button, pos[0], pos[1], Qt.AlignCenter)

        # Setup
        selected_sound_playback_layout.addWidget(selected_sound_play_button)
        selected_sound_playback_layout.addWidget(selected_sound_display)

    def report(self):
        self.sound_button_group.report()
