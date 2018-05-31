#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-28

Reference for style conventions : https://www.python.org/dev/peps/pep-0008
"""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton

from Config import Config


class LoadingTime(QWidget):
    """Widget that shows a message and a spinner or a progress bar, to be shown while the program
    is processing/loading."""

    def __init__(self):
        super().__init__()
        self.init_ui()

        # This will disable input on all other windows
        self.setWindowModality(Qt.ApplicationModal)

        self.setWindowFlags(Qt.FramelessWindowHint)

    def init_ui(self):
        spinner_label = QLabel()
        spinner_movie = QMovie("images/spinner.gif")
        spinner_label.setMovie(spinner_movie)
        spinner_label.show()
        spinner_movie.start()
        spinner_layout = QHBoxLayout()
        spinner_layout.addStretch(1)
        spinner_layout.addWidget(spinner_label)
        spinner_layout.addStretch(1)

        text_label = QLabel(Config.LOADING_TEXT)
        text_layout = QHBoxLayout()
        text_layout.addStretch(1)
        text_layout.addWidget(text_label)
        text_layout.addStretch(1)

        self.back_button = QPushButton(Config.CANCEL_IA_TEXT)
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.back_button)

        layout = QVBoxLayout()
        layout.addLayout(spinner_layout)
        layout.addLayout(text_layout)
        layout.addLayout(button_layout)
        self.setLayout(layout)

