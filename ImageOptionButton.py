#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-17

Reference for style conventions : https://www.python.org/dev/peps/pep-0008
"""

from PyQt5.QtCore import pyqtSignal

from Config import Config
from ImageButton import ImageButton


class ImageOptionButton(ImageButton):
    """This is an :py:class:`ImageButton` that is checkable (option button). A name has to be given to this button,
    for identification convenience"""

    selected = pyqtSignal()
    """This signal is emited when the button gets selected"""

    def __init__(self, img_path, name):
        super().__init__(img_path, is_round=False)  # ImageOptionButtons should never be round
        self.name = name

        self.setCheckable(True)
        self.setAutoExclusive(True)

        self._set_style_()

    def _set_style_(self):
        self.setStyleSheet("""
            ImageOptionButton
            {
                padding: 4px 2px 4px 2px;
                border: none;
                background-color: rgba(0, 0, 0, 0%);
            }
            ImageOptionButton:pressed
            {
                background-color: #cccccc;
            }
            ImageOptionButton:checked
            {
                border: 4px solid """ + Config.BORDER_BLUE + """;
            }
            """)

    def get_name(self):
        """Return the name of the button"""
        return self.name
