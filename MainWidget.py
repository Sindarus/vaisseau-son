#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-22

Reference for style conventions : https://www.python.org/dev/peps/pep-0008/#naming-conventions
"""
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox

from CaptionedImageButton import CaptionedImageButton
from Config import Config
from LoadingTime import LoadingTime
from ResultsWindow import ResultsWindow
from SoundChooser import SoundChooser
from SoundRecorder import SoundRecorder
from SoundClassifier import SoundClassifier


class MainWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

        self.loading_window = LoadingTime()
        self.loading_window.back_button.clicked.connect(self.interrupt)
        self.results_window = ResultsWindow()
        self.results_window.back_arrow.clicked.connect(self.results_window.hide)
        self.results_window.reload_arrow.clicked.connect(self.reset)

    def init_ui(self):
        # Create sound chooser and recorder widgets
        title = QLabel(Config.TITLE, self)
        self.sound_chooser = SoundChooser(self)
        self.sound_recorder = SoundRecorder(self)

        # Create go button
        self.go_button = CaptionedImageButton(Config.VALIDATE_BUTTON,
                                              "images/right-arrow.png",
                                              "images/right-arrow-disabled.png")
        self.go_button.set_disabled(True)
        self.sound_recorder.player_recorder.was_recorded.connect(lambda: self.go_button.set_disabled(False))
        self.go_button.resize_image(Config.NAV_ICON_SIZE, Config.NAV_ICON_SIZE)
        self.go_button.clicked.connect(self.process_comparison)

        # Create reload button
        reload_button = CaptionedImageButton(Config.RELOAD_ICON_TEXT, "images/reload.png")
        reload_button.resize_image(Config.NAV_ICON_SIZE, Config.NAV_ICON_SIZE)
        reload_button.clicked.connect(self.reset)

        # Create Layouts
        main_layout = QVBoxLayout()
        title_layout = QHBoxLayout()
        buttons_layout = QHBoxLayout()

        # Setup main layout
        self.setLayout(main_layout)
        main_layout.addLayout(title_layout)
        main_layout.addWidget(self.sound_chooser)
        main_layout.addWidget(self.sound_recorder)
        main_layout.addStretch(1)
        main_layout.addLayout(buttons_layout)

        # Setup title
        title_layout.addStretch(1)
        title_layout.addWidget(title)
        title_layout.addStretch(1)

        # Setup go_button
        buttons_layout.addWidget(reload_button)
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(self.go_button)

    def process_comparison(self):
        rec_sound_path = self.sound_recorder.player_recorder.get_recorded_sound_path()
        selected_sound_name = self.sound_chooser.get_selected_sound_name()
        selected_sound_path = Config.SOUNDS[selected_sound_name]['sound_path']
        print("comparing", rec_sound_path, "to", selected_sound_path)

        self.loading_window.show()
        classifier = SoundClassifier(rec_sound_path, self.show_results)
        classifier.start()

    def show_results(self, results):
        print("show_results called in", current_thread())
        print(results)
        self.loading_window.hide()
        self.results_window.showFullScreen() if Config.FULLSCREEN else self.results_window.show()

    def close_child_windows(self):
        self.loading_window.hide()

    def interrupt(self):
        self.loading_window.hide()
        print("processing was interrupted")
        # TODO: halt processing

    def reset(self):
        self.results_window.hide()
        print("reset")
        # TODO: reset
