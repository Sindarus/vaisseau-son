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
from LoadingTimeWindow import LoadingTimeWindow
from MessageDisplay import MessageDisplay
from ResultsWindow import ResultsWindow
from Imitation import Imitation
from SoundChooser import SoundChooser
from SoundClassifier import SoundClassifier
from SoundRecorder import SoundRecorder
from sound_db_connector import SoundDBConnector


class MainWidget(QWidget):
    """QWidget that displays the sound chooser, the sound recorder, the reset button and a "next" button.

    This widget also deals with calling a new thread for sound processing through the three methods
    :py:func:`step1_process_comparison`, :py:func:`step2_wait_for_results` and :py:func:`step3_show_results`. Those
    three methods are called in sequence : the "go" button is connected to the :py:func:`step1_process_comparison`
    method, which starts a new thread, shows a waiting window with a spinner, and then calls
    :py:func:`step2_wait_for_results`. :py:func:`step2_wait_for_results` implements a loop for pooling the status of
    the thread, by calling itself again if the thread is not finished yet. When the thread is finished,
    :py:func:`step2_wait_for_results` calls :py:func:`step3_show_results` which displays the result window.

    *self.results*: results of the processing. This variable should be a list of 2-tuples containing the name
    of the sound and the probability that the user tried to imitate this sound. example: [("lion", 85), ("police",
    20), ("cow", 5), ("wind", 3)]

    *self.classifier*: runable thread that holds the sound processing algorithm, loaded in
    :py:func:`step1_process_comparison`."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_ui()

        self.results = None
        self.cur_imitation = None

        self.loading_window = LoadingTimeWindow()
        self.loading_window.back_button.clicked.connect(self.interrupt)
        self.results_window = ResultsWindow()
        self.results_window.back_arrow.clicked.connect(self.results_window.hide)
        self.results_window.reload_arrow.clicked.connect(self.full_reset)
        self.results_window.window_shown.connect(self.parentWidget().hide)
        self.results_window.window_hidden.connect(self.parentWidget().show)

        self.sound_db = SoundDBConnector()

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
        self.sound_recorder.player_recorder.was_recorded.connect(
            lambda: self.notif_zone.setText(""))
        self.sound_recorder.player_recorder.recording_started.connect(
            # record previous sound if existing
            lambda: self.save_cur_imitation(submitted=False, skip_missing=True))
        self.sound_recorder.player_recorder.recording_started.connect(self.load_imitation)
        self.sound_recorder.player_recorder.recording_started.connect(
            lambda: self.notif_zone.setText(Config.CURRENTLY_RECORDING_MSG))
        self.go_button.resize_image(Config.NAV_ICON_SIZE, Config.NAV_ICON_SIZE)
        self.go_button.clicked.connect(
            lambda: self.save_cur_imitation(submitted=True, skip_missing=False))
        self.go_button.clicked.connect(self.step1_process_comparison)

        # Create reload button
        reload_button = LabeledImageButton(Config.RELOAD_ICON_TEXT, "images/reload.png")
        reload_button.resize_image(Config.NAV_ICON_SIZE, Config.NAV_ICON_SIZE)
        reload_button.clicked.connect(self.full_reset)

        # Create message display widget
        self.notif_zone = MessageDisplay()
        self.notif_zone.setStyleSheet("""
            QLabel {
                font-size: 24px;
                color: #ff0000;
            }
        """)

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

    @pyqtSlot()
    def step1_process_comparison(self):
        """Start classifier in a new thread, show a loading window and call the :py:func`step2_wait_for_result` routine.

        This function retrieves the path of the sound that was recorded by the user, loads a new
        :py:class:`SoundClassifier` object with this path, and launches the processing. It also shows a loading
        window with a spinner while the processing is ongoing, and calls the :py:func`step2_wait_for_results
        function.`"""
        rec_sound_path = self.sound_recorder.player_recorder.get_recorded_sound_path()
        selected_sound_name = self.sound_chooser.get_selected_sound_name()
        selected_sound_path = Config.SOUNDS[selected_sound_name]['sound_path']
        print("comparing", rec_sound_path, "to", selected_sound_path)

        self.classifier = SoundClassifier(rec_sound_path, self.set_results)
        self.classifier.start()
        self.step2_wait_for_results(self.classifier.ident)
        self.loading_window.show()

    def step2_wait_for_results(self, ident_classifier_thread):
        """Wait for the sound classifier thread to be finished and calls :py:func`step3_show_results`.

        The *ident_classifier_thread* argument should be the ident of the thread that this function is waiting for.
        When this function is called, it creates a loop (using :py:func`QTimer.singleShot`). If the user demands to
        cancel the classifying process, *self.classifier.should_stop* will be set to 1 and the
        :py:func`step2_wait_for_results` will know that it should stop its loop. If however the user has demanded a
        new classifying process to start, *self.classifier.should_stop* will be false, but the *self.classifier.ident*
        will be different, and the :py:func`step2_wait_for_results` will still know it should stop its loop."""
        if self.classifier.ident != ident_classifier_thread or self.classifier.should_stop:
            return
            # this defuses this wait_for_results loop, because the classifier we were waiting for has been canceled
            # or was replaced by a new one that has its own dedicated wait_for_results loop
        elif self.classifier.is_alive():
            QTimer.singleShot(500, lambda: self.step2_wait_for_results(ident_classifier_thread))
        else:
            self.step3_show_results()

    def step3_show_results(self):
        """Load results into the result window then show it.

        This function is called by :py:func`step2_wait_for_results` when the sound classifier proccess is finished.
        It loads the results into the :py:class:`ResultsWindow` and then show the said window."""
        assert self.results is not None, "No results to show"
        print("results:", self.results)
        self.loading_window.hide()
        self.results_window.load_results(self.results)
        self.results_window.showFullScreen() if Config.FULLSCREEN else self.results_window.show()

    def load_imitation(self, temp_path, datetime):
        label = self.sound_chooser.get_selected_sound_name()
        self.cur_imitation = Imitation(temp_path, label, datetime)

    def save_cur_imitation(self, submitted, skip_missing):
        if self.cur_imitation is None:
            if skip_missing:
                return
            else:
                raise AssertionError("Trying to save a sound but none was recorded and skip_missing is set to False")
        else:
            self.cur_imitation.save(self.sound_db, submitted)

    def set_results(self, results):
        """Set the results instance variable to what has been passed in argument.

        Function called by the classifier thread to return its results. Albeit this function is run in another thread,
        it does update the instance variable that is then accessible by the main thread."""
        self.results = results

    def close_child_windows(self):
        """Hide or close windows that were created by this class"""
        self.loading_window.hide()
        self.results_window.hide()

    @pyqtSlot()
    def interrupt(self):
        """Interrupt classifier thread"""
        self.loading_window.hide()
        self.classifier.please_stop_asap()

    @pyqtSlot()
    def full_reset(self):
        """Reset the entire UI"""
        self.reset()
        self.sound_recorder.player_recorder.reset()
        self.results_window.hide()
        self.results_window.reset()

    def reset(self):
        # Save current imitation if existing, before wiping it
        self.save_cur_imitation(submitted=False, skip_missing=True)
        self.cur_imitation = None

    def after_show_init(self):
        """Performs initializations that needs to be done after the main window has been shown"""
        self.sound_chooser.after_show_init()
