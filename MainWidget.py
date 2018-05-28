#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-22

Reference for style conventions : https://www.python.org/dev/peps/pep-0008/#naming-conventions
"""
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (QWidget,
                             QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel)

from Config import Config
from LoadingTime import LoadingTime
from SoundChooser import SoundChooser
from SoundRecorder import SoundRecorder


class MainWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

        self.loading_window = LoadingTime()
        self.loading_window.back_button.clicked.connect(self.interrupt)

    def init_ui(self):
        # Create widgets
        title = QLabel(Config.TITLE, self)
        button = QPushButton(Config.VALIDATE_BUTTON, self)
        self.sound_chooser = SoundChooser(self)
        sound_recorder = SoundRecorder(self)

        # Create Layouts
        main_layout = QVBoxLayout()
        title_layout = QHBoxLayout()
        button_layout = QHBoxLayout()

        # Setup main layout
        self.setLayout(main_layout)
        main_layout.addLayout(title_layout)
        main_layout.addWidget(self.sound_chooser)
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

        button.clicked.connect(self.process_comparison)

    def process_comparison(self):
        rec_sound_path = None
        selected_sound_path = None

        self.loading_window.show()
        # TODO: Start comparing sounds
        QTimer.singleShot(5000, self.show_results)

    def show_results(self):
        self.loading_window.hide()
        self.results_window.show()

    def close_child_windows(self):
        self.loading_window.hide()

    def interrupt(self):
        self.loading_window.hide()
        print("processing was interrupted")
        # TODO: halt processing
