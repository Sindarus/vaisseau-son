#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-23

Reference for style conventions : https://www.python.org/dev/peps/pep-0008
"""

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QPushButton

from Config import Config


class ImageButton(QPushButton):

    def __init__(self, img_path, is_round=True):
        super().__init__()

        self.img_path = img_path
        self.img = QPixmap(img_path)
        self.width = self.img.width()
        self.height = self.img.height()

        icon = QIcon(self.img)
        self.setIcon(icon)

        self.is_round = is_round  # Is the image round ?

        self._set_style()

    def resize_image(self, width, height):
        self.setIconSize(QSize(width, height))
        self.width = width
        self.height = height

        if self.is_round:
            self.update_round_style()

    def change_image(self, img_path):
        self.img = QPixmap(img_path)
        icon = QIcon(self.img)
        self.setIcon(icon)

    def update_round_style(self):
        # we have to pick the minimum of the two sizes, otherwise, the border-radius property will be ignored
        self._set_style(border_radius=str(min(self.width, self.height) // 2) + "px")
        # reload style
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

    def _set_style(self, border_radius="0px"):
        self.setStyleSheet("""
            ImageButton
            {
                padding: 2px 0px 2px 0px;
                border: none;
                background-color: rgba(0, 0, 0, 0%);
            }
            ImageButton:pressed
            {
                border: """ + str(Config.IMAGE_BUTTON_HOLD_BORDER_WIDTH) + """px solid """ + Config.BORDER_BLUE + """;
                border-radius: """ + border_radius + """;
                background-color: #cccccc;
            }
            """)

    def __repr__(self):
        return "ImageButton : " + str(self.img_path)
