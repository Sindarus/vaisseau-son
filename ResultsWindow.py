#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-28

Reference for style conventions : https://www.python.org/dev/peps/pep-0008
"""

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QWidget, QShortcut, qApp, QHBoxLayout, QVBoxLayout, QDesktopWidget, QSizePolicy

from CaptionedImage import CaptionedImage
from Config import Config
from CustomStyleGroupBox import CustomStyleGroupBox
from LabeledImageButton import LabeledImageButton


class ResultsWindow(QWidget):
    """Window to display the results of the classification process"""

    window_shown = pyqtSignal()
    """Signal that is emited when the "show" method is called. Needed for the main window to hide itself on time."""
    window_hidden = pyqtSignal()
    """Signal that is emited when the "hide" method is called. Needed for the main window to show itself on time."""

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setGeometry(0, 0, Config.WINDOW_MODE_WIDTH, Config.WINDOW_MODE_HEIGHT)

        # This will disable input on all other windows
        self.setWindowModality(Qt.ApplicationModal)

        # actions
        self.quit_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_Q), self)
        self.quit_shortcut.activated.connect(qApp.quit)

        self._set_style()

    def init_ui(self):
        self.main_result_layout = QHBoxLayout()
        self.extra_results_layout = QHBoxLayout()

        layout = QVBoxLayout()
        layout.addLayout(self.main_result_layout)
        layout.addLayout(self.extra_results_layout)
        self.init_results_widgets()

        results_group = CustomStyleGroupBox(Config.RESULTS_GROUP_TEXT)
        results_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        results_group.setLayout(layout)

        self.back_arrow = LabeledImageButton(Config.BACK_ARROW_TEXT, "images/left-arrow.png")
        self.back_arrow.resize_image(Config.NAV_ICON_SIZE, Config.NAV_ICON_SIZE)
        self.reload_arrow = LabeledImageButton(Config.RELOAD_ICON_TEXT, "images/reload.png")
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

    def init_results_widgets(self):
        self.main_result_widget = CaptionedImage()
        self.main_result_widget.resize_image(Config.MAIN_RESULT_IMAGE_SIZE, Config.MAIN_RESULT_IMAGE_SIZE)
        self.main_result_widget.setStyleSheet("""
            QLabel{
                background-color: rgba(0, 0, 0, 0%);
                font-size: 24px;
            }
        """)
        self.main_result_layout.addStretch(1)
        self.main_result_layout.addWidget(self.main_result_widget)
        self.main_result_layout.addStretch(1)

        self.extra_results_widgets = []
        for i in range(3):
            cur_result_widget = CaptionedImage()
            cur_result_widget.resize_image(Config.EXTRA_RESULT_IMAGE_SIZE, Config.EXTRA_RESULT_IMAGE_SIZE)
            self.extra_results_widgets.append(cur_result_widget)
            self.extra_results_layout.addWidget(cur_result_widget)

    def load_results(self, results):
        """Load result data in display widgets

        *results* must be a list of 2-tuples containing the name of the sound and the probability"""

        # Only keep the first 4 results (this operation will not alter the list objet in argument)
        results = results[:4]

        # Adding main result
        (main_result_name, main_result_percent) = results.pop(0)
        main_result_display_name = Config.SOUNDS[main_result_name]['display_name']
        main_result_img_path = Config.SOUNDS[main_result_name]['image_path']
        self.main_result_widget.load_caption(Config.RESULT_ITEM_TEXT % (main_result_display_name, main_result_percent))
        self.main_result_widget.load_image(main_result_img_path)

        # Adding extra results
        for i, result in enumerate(results):
            (result_name, result_percent) = result
            result_img_path = Config.SOUNDS[result_name]['image_path']
            self.extra_results_widgets[i].load_caption(Config.EXTRA_RESULT_ITEM_TEXT % result_percent)
            self.extra_results_widgets[i].load_image(result_img_path)

    def _center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def reset(self):
        """Unload results from the display widgets."""
        self.main_result_widget.clear()
        for cur_result_widget in self.extra_results_widgets:
            cur_result_widget.clear()

    def show(self):
        self.window_shown.emit()
        super().show()

    def hideEvent(self, e):
        self.window_hidden.emit()
        super().hideEvent(e)

    def _set_style(self):
        self.setStyleSheet("""
            ResultsWindow {
                background: """ + Config.LIGHT_LIGHT_BLUE + """;
                color: """ + Config.FONT_COLOR + """;
            }
        """)
