#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-22

Reference for style conventions : https://www.python.org/dev/peps/pep-0008/#naming-conventions
"""

from PyQt5.QtWidgets import (QWidget,
                             QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel)

from SoundChooser import SoundChooser
from SoundRecorder import SoundRecorder


class MainWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Create widgets
        title = QLabel("Atelier son", self)
        button = QPushButton("Envoyer", self)
        sound_chooser = SoundChooser(self)
        sound_recorder = SoundRecorder(self)

        # Create Layouts
        main_layout = QVBoxLayout()
        title_layout = QHBoxLayout()
        button_layout = QHBoxLayout()

        # Setup main layout
        self.setLayout(main_layout)
        main_layout.addLayout(title_layout)
        main_layout.addWidget(sound_chooser)
        main_layout.addWidget(sound_recorder)
        main_layout.addStretch(1)
        main_layout.addLayout(button_layout)

        # Setup title
        title_layout.addStretch(1)
        title_layout.addWidget(title)
        title_layout.addStretch(1)

        # Setup button
        button_layout.addStretch(1)
        button_layout.addWidget(button)

        button.clicked.connect(lambda: sound_chooser.report())
