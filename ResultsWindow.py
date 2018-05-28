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
        main_result = CaptionedImage("L'IA a reconnu un rugissement\navec une certitude de 93%.", "images/lion.png")
        main_result.resize_image(Config.MAIN_RESULT_IMAGE_SIZE, Config.MAIN_RESULT_IMAGE_SIZE)
        extra_results = [CaptionedImage("L'IA a reconnu une sirène de police\navec une certitude de 22%.",
                                        "images/police.png"),
                         CaptionedImage("L'IA a reconnu un beuglement\navec une certitude de 13%.",
                                        "images/cow.png"),
                         CaptionedImage("L'IA a reconnu un sifflement de vent\navec une certitude de 3%.",
                                        "images/wind.png")]
        for result in extra_results:
            result.resize_image(Config.EXTRA_RESULT_IMAGE_SIZE, Config.EXTRA_RESULT_IMAGE_SIZE)

        main_result_layout = QHBoxLayout()
        main_result_layout.addStretch(1)
        main_result_layout.addWidget(main_result)
        main_result_layout.addStretch(1)

        extra_results_layout = QHBoxLayout()
        for result in extra_results:
            extra_results_layout.addWidget(result)

        layout = QVBoxLayout()
        layout.addLayout(main_result_layout)
        layout.addLayout(extra_results_layout)

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

    def _center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
