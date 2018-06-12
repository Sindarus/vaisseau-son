#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-29

Reference for style conventions : https://www.python.org/dev/peps/pep-0008
"""

import time
from threading import Thread


class SoundClassifier(Thread):
    """Thread that contains the classifying logic"""

    def __init__(self, user_sound_path, set_results_func):
        super().__init__()
        self.user_sound_path = user_sound_path
        self.set_results_func = set_results_func
        self.should_stop = False  # Is set to True if someone requested that this thread terminates asap

    def run(self):
        """Is called when the threads is started"""
        time.sleep(3)
        # TODO: do some real calculation
        results = [("lion", 85), ("police", 20), ("cow", 5), ("wind", 3)]
        if self.should_stop:
            return
        self.set_results_func(results)

    def please_stop_asap(self):
        """Tell this thread to stop as soon as possible.

        This is indeed the prefered method to stop a thread :
        https://stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread-in-python#325528"""
        self.should_stop = True
        # TODO: In the "run" function, check this value on a regular basis so that the thread can stop itself.
        # TODO: If this is not done properly, there's a risk that the thread will remain alive even after all other
        # TODO: windows have been closed, until run() reaches an end.
