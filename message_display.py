#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-31

Reference for style conventions : https://www.python.org/dev/peps/pep-0008
"""

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QLabel


class MessageDisplay(QLabel):
    """Simple Widget to display a message and erase it automatically after a given time."""

    def __init__(self):
        super().__init__()

    def display_text(self, text, timeout):
        """Load a text"""
        self.setText(text)
        QTimer.singleShot(timeout, lambda: self.clear())

    def _set_style(self):
        self.setStyleSheet("""
            MessageDisplay {
                border: 5px solid red;
            }
        """)
