#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-31

Reference for style conventions : https://www.python.org/dev/peps/pep-0008/#naming-conventions
"""
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QLabel


class MessageDisplay(QLabel):

    def __init__(self):
        super().__init__()

    def display_text(self, text, timeout):
        self.setText(text)
        QTimer.singleShot(timeout, lambda: self.clear())

    def _set_style(self):
        self.setStyleSheet("""
            QFrame, QLabel, QToolTip {
                border: 5px solid red;
            }
            """)
