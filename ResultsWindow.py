#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-28

Reference for style conventions : https://www.python.org/dev/peps/pep-0008/#naming-conventions
"""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QWidget, QShortcut, qApp, QHBoxLayout, QVBoxLayout, QDesktopWidget, QGroupBox

from CaptionedImage import CaptionedImage
from Config import Config


class ResultsWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

        # actions
        self.quit_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_Q), self)
        self.quit_shortcut.activated.connect(qApp.quit)

    def init_ui(self):
        self.main_result_layout = QHBoxLayout()
        self.extra_results_layout = QHBoxLayout()

        layout = QVBoxLayout()
        layout.addLayout(self.main_result_layout)
        layout.addLayout(self.extra_results_layout)

        results_group = QGroupBox(Config.RESULTS_GROUP_TEXT)
        results_group.setLayout(layout)

        self.back_arrow = CaptionedImage(Config.BACK_ARROW_TEXT, "images/left-arrow.png")
        self.back_arrow.resize_image(Config.NAV_ICON_SIZE, Config.NAV_ICON_SIZE)
        self.reload_arrow = CaptionedImage(Config.RELOAD_ICON_TEXT, "images/reload.png")
        self.reload_arrow.resize_image(Config.NAV_ICON_SIZE, Config.NAV_ICON_SIZE)

        nav_icons_layout = QHBoxLayout()
        nav_icons_layout.addWidget(self.back_arrow)
        nav_icons_layout.addWidget(self.reload_arrow)
        nav_icons_layout.addStretch(1)

        main_layout = QVBoxLayout()
        main_layout.addWidget(results_group)
        main_layout.addLayout(nav_icons_layout)
        self.setLayout(main_layout)

        self._center()

    def load_results(self, results):
        """Results must be a list of 2-tuples containing the name of the sound and the probability"""

        # Adding main result
        (main_result_name, main_result_percent) = results.pop(0)
        main_result_display_name = Config.SOUNDS[main_result_name]['display_name']
        main_result_img_path = Config.SOUNDS[main_result_name]['image_path']
        main_result_widget = CaptionedImage(Config.RESULT_ITEM_TEXT % (main_result_display_name, main_result_percent),
                                            main_result_img_path)
        main_result_widget.resize_image(Config.MAIN_RESULT_IMAGE_SIZE, Config.MAIN_RESULT_IMAGE_SIZE)
        self.main_result_layout.addStretch(1)
        self.main_result_layout.addWidget(main_result_widget)
        self.main_result_layout.addStretch(1)

        # Adding extra results
        for result in results:
            (result_name, result_percent) = result
            result_img_path = Config.SOUNDS[result_name]['image_path']
            result_widget = CaptionedImage(Config.EXTRA_RESULT_ITEM_TEXT % result_percent, result_img_path)
            result_widget.resize_image(Config.EXTRA_RESULT_IMAGE_SIZE, Config.EXTRA_RESULT_IMAGE_SIZE)
            self.extra_results_layout.addWidget(result_widget)

    def _center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
