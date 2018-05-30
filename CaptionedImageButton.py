#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-30

Reference for style conventions : https://www.python.org/dev/peps/pep-0008/#naming-conventions
"""

from CaptionedImage import CaptionedImage


class CaptionedImageButton(CaptionedImage):

    def __init__(self, text, image_path, image_path_disabled=None):
        super().__init__(text, image_path)
        self.disabled = False
        self.image_path = image_path
        self.image_path_disabled = image_path_disabled

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        if not self.disabled:
            self.clicked.emit()

    def set_disabled(self, state):
        self.disabled = state
        if (state is True) and (self.image_path_disabled is not None):
            self.change_image(self.image_path_disabled)
        if (state is False) and (self.image_path_disabled is not None):
            self.change_image(self.image_path)
