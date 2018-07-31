#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-23

Reference for style conventions : https://www.python.org/dev/peps/pep-0008
"""

from PyQt5.QtWidgets import QHBoxLayout

from audio_player import AudioPlayer
from custom_style_groupbox import CustomStyleGroupBox


class SoundRecorder(CustomStyleGroupBox):
    """Widget that allows the user to record a sound, to listen to it and to visualize it"""

    def __init__(self, parent_widget):
        super().__init__("Enregistrer un son", parent_widget)
        self.init_ui()

    def init_ui(self):
        self.player_recorder = AudioPlayer(recordable=True)
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.player_recorder)

        self.setLayout(self.layout)
