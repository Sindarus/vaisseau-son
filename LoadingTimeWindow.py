#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-28

Reference for style conventions : https://www.python.org/dev/peps/pep-0008
"""

from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QDesktopWidget

from Config import Config
from LabeledImageButton import LabeledImageButton


class LoadingTimeWindow(QWidget):
    """Widget that shows a message and a spinner to be shown while the program is processing/loading.

    It is meant to be used as a modal window."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_ui()
        self._set_style()

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

        self.back_button = LabeledImageButton(Config.CANCEL_IA_TEXT, "images/left-arrow.png")
        self.back_button.resize_image(Config.LITTLE_NAV_ICON_SIZE, Config.LITTLE_NAV_ICON_SIZE)
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.back_button)

        layout = QVBoxLayout()
        layout.addLayout(spinner_layout)
        layout.addLayout(text_layout)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def center(self):
        """Center the window in relation to its parent widget, or the screen, if the app is in fullscreen."""
        self_rect = self.frameGeometry()
        if Config.FULLSCREEN:
            reference_rect = QDesktopWidget().availableGeometry()
        else:
            reference_rect = QRect(0, 0, Config.WINDOW_MODE_WIDTH, Config.WINDOW_MODE_HEIGHT)
        center_point = reference_rect.center()
        self_rect.moveCenter(center_point)

        self.move(self_rect.topLeft())

    def showEvent(self, a):
        """Extend showEvent handler function to automatically center this window when is is shown."""
        super().showEvent(a)
        self.center()

    def _set_style(self):
        self.setStyleSheet("""
            LoadingTimeWindow {
                background: """ + Config.LIGHT_LIGHT_BLUE + """;
                color: """ + Config.FONT_COLOR + """;
            }
        """)