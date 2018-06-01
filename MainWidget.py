#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-22

Reference for style conventions : https://www.python.org/dev/peps/pep-0008
"""

from PyQt5.QtCore import QTimer, pyqtSlot
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel

from Config import Config
from LabeledImageButton import LabeledImageButton
from LoadingTime import LoadingTime
from MessageDisplay import MessageDisplay
from ResultsWindow import ResultsWindow
from SoundChooser import SoundChooser
from SoundClassifier import SoundClassifier
from SoundRecorder import SoundRecorder


class MainWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

        self.results = None  # Results of the classifying process

        self.loading_window = LoadingTime()
        self.loading_window.back_button.clicked.connect(self.interrupt)
        self.results_window = ResultsWindow()
        self.results_window.back_arrow.clicked.connect(self.results_window.hide)
        self.results_window.reload_arrow.clicked.connect(self.full_reset)

    def init_ui(self):
        # Create sound chooser and recorder widgets
        title = QLabel(Config.TITLE, self)
        title.setStyleSheet("""
            QLabel{
                font-size: 24px;
            }
        """)
        self.sound_chooser = SoundChooser(self)
        self.sound_recorder = SoundRecorder(self)

        # Create go button
        self.go_button = LabeledImageButton(Config.VALIDATE_BUTTON, "images/right-arrow.png")
        self.go_button.setEnabled(False)
        self.sound_recorder.player_recorder.was_recorded.connect(lambda: self.go_button.setEnabled(True))
        self.go_button.resize_image(Config.NAV_ICON_SIZE, Config.NAV_ICON_SIZE)
        self.go_button.clicked.connect(self.step1_process_comparison)

        # Create reload button
        reload_button = LabeledImageButton(Config.RELOAD_ICON_TEXT, "images/reload.png")
        reload_button.resize_image(Config.NAV_ICON_SIZE, Config.NAV_ICON_SIZE)
        reload_button.clicked.connect(self.full_reset)

        # Create message display widget
        self.notif_zone = MessageDisplay()
        self.sound_recorder.player_recorder.recorded_too_short.connect(self.recorded_too_short_action)

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

        # Setup nav buttons
        buttons_layout.addWidget(reload_button)
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(self.notif_zone)
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(self.go_button)

    def step1_process_comparison(self):
        rec_sound_path = self.sound_recorder.player_recorder.get_recorded_sound_path()
        selected_sound_name = self.sound_chooser.get_selected_sound_name()
        selected_sound_path = Config.SOUNDS[selected_sound_name]['sound_path']
        print("comparing", rec_sound_path, "to", selected_sound_path)

        self.classifier = SoundClassifier(rec_sound_path, self.set_results)
        self.classifier.start()
        self.step2_wait_for_results(self.classifier.ident)
        self.loading_window.show()
        self.loading_window.center()

    def step2_wait_for_results(self, ident_classifier_thread):
        if self.classifier.ident != ident_classifier_thread or self.classifier.should_stop:
            return
            # this defuses this wait_for_results loop, because the classifier we were waiting for has been canceled
            # or was replaced by a new one that has its own dedicated wait_for_results loop
        elif self.classifier.is_alive():
            QTimer.singleShot(500, lambda: self.step2_wait_for_results(ident_classifier_thread))
        else:
            self.step3_show_results()

    def step3_show_results(self):
        assert self.results is not None, "No results to show"
        print("results:", self.results)
        self.loading_window.hide()
        self.results_window.load_results(self.results)
        self.results_window.showFullScreen() if Config.FULLSCREEN else self.results_window.show()

    def set_results(self, results):
        self.results = results

    def close_child_windows(self):
        self.loading_window.hide()

    def interrupt(self):
        self.loading_window.hide()
        self.classifier.please_stop_asap()

    def full_reset(self):
        self.sound_recorder.player_recorder.reset()
        self.results_window.hide()
        self.results_window.reset()

    def after_show_init(self):
        self.sound_chooser.after_show_init()

    @pyqtSlot()
    def recorded_too_short_action(self):
        self.notif_zone.display_text(Config.REC_TOO_SHORT_TOOLTIP_MSG, Config.NOTIFICATION_MESSAGES_TIMEOUT)
        self.go_button.setEnabled(False)
