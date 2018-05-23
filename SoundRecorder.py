#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-23

Reference for style conventions : https://www.python.org/dev/peps/pep-0008/#naming-conventions
"""

from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGroupBox

from ImageButton import ImageButton
from WaveformDisplay import WaveformDisplay


class SoundRecorder(QGroupBox):
    """Widget that allows the user to record a sound, to listen to it and to visualize it"""

    def __init__(self, parent_widget):
        super().__init__("Enregistrer un son", parent_widget)
        self.init_ui()

    def init_ui(self):
        # Create widgets
        sound_display = WaveformDisplay()
        sound_display.load_audio("232289__zglar__zombie-or-monster-or-lion-roar.wav")
        sound_play_button = ImageButton("images/play2.png")
        sound_play_button.resize_image(100, 100)
        sound_rec_button = ImageButton("images/record.png")
        sound_rec_button.resize_image(100, 100)

        # Create layouts
        sound_playback_layout = QHBoxLayout()
        playrec_buttons_layout = QVBoxLayout()

        # Setup main layout
        self.setLayout(sound_playback_layout)
        sound_playback_layout.addLayout(playrec_buttons_layout)
        sound_playback_layout.addWidget(sound_display)

        # Setup layout for play and rec buttons
        playrec_buttons_layout.addWidget(sound_play_button)
        playrec_buttons_layout.addWidget(sound_rec_button)
