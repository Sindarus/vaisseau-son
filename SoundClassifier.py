#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-29

Reference for style conventions : https://www.python.org/dev/peps/pep-0008/#naming-conventions
"""

import time
from threading import Thread


class SoundClassifier(Thread):

    def __init__(self, user_sound_path, set_results_func):
        super().__init__()
        self.user_sound_path = user_sound_path
        self.set_results_func = set_results_func

    def run(self):
        time.sleep(3)
        # TODO: do some real calculation
        results = [("lion", 85), ("police", 20), ("cow", 5), ("wind", 3)]
        self.set_results_func(results)
