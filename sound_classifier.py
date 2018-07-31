#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-29

Reference for style conventions : https://www.python.org/dev/peps/pep-0008
"""

from threading import Thread

from config import Config
from ai_running_unit import AIRunningUnit
from feature_extractor import FeatureExtractor


class SoundClassifier(Thread):
    """Thread that contains the classifying logic"""

    def __init__(self, user_sound_path, set_results_func):
        super().__init__()
        self.user_sound_path = user_sound_path
        self.set_results_func = set_results_func
        self.should_stop = False  # Is set to True if someone requested that this thread terminates asap

        self.my_feat_extr = FeatureExtractor()
        self.my_feat_extr.config(do_deltas=True, do_squares=False)
        self.ai = AIRunningUnit(Config.MODEL_DIR_PATH)

    def run(self):
        """Is called when the thread is started"""
        if self.should_stop:
            return
        self.my_feat_extr.load_file(self.user_sound_path)
        if self.should_stop:
            return
        self.features = self.my_feat_extr.get_features(as_dict=True)
        if self.should_stop:
            return
        self.probas = self.ai.predict(self.features)
        if self.should_stop:
            return
        results = [(Config.SOUND_NAME_NUMBER[i], int(proba*100)) for i, proba in enumerate(self.probas)]
        if self.should_stop:
            return
        self.set_results_func(results)
        return

    def please_stop_asap(self):
        """Tell this thread to stop as soon as possible.

        This is indeed the prefered method to stop a thread :
        https://stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread-in-python#325528"""
        self.should_stop = True
