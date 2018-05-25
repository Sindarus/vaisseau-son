#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-17

Reference for style conventions : https://www.python.org/dev/peps/pep-0008/#naming-conventions
"""

from PyQt5.QtCore import pyqtSlot, QObject


class ImageOptionButtonGroup(QObject):

    def __init__(self):
        super().__init__()
        self.image_buttons = []
        self.id_selected = None

    def add_image_button(self, button):
        self.image_buttons.append(button)
        button.selected.connect(self.button_was_clicked)

    @pyqtSlot()
    def button_was_clicked(self):
        for i, image_button in enumerate(self.image_buttons):
            if image_button != self.sender():
                image_button.unselect()
            else:
                self.id_selected = i

    def get_id_selected(self):
        """Returns the id of the button that is currently selected. Buttons are assigned IDs according to the order
        they were added to the group.
        Warning: returns None if no button was selected"""
        return self.id_selected
