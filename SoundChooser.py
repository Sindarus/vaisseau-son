#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-22

Reference for style conventions : https://www.python.org/dev/peps/pep-0008/#naming-conventions
"""

from PyQt5.QtCore import Qt, QUrl, pyqtSlot
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox

from ImageButton import ImageButton
from ImageOptionButton import ImageOptionButton
from ImageOptionButtonGroup import ImageOptionButtonGroup
from WaveformDisplay import WaveformDisplay


class SoundChooser(QGroupBox):
    """Widget that allows the user to choose a sound from a set, and to listen to it"""

    def __init__(self, parent_widget):
        super().__init__("Choisir un son", parent_widget)

        self.sound_bank = []  # list of dict containing the path to the sound and the path to the image
        self.sound_bank.append({'sound_path': "sounds/232289__zglar__zombie-or-monster-or-lion-roar.wav",
                                'image_path': "images/lion.png"})
        self.sound_bank.append({'sound_path': "sounds/58277__benboncan__cow.wav",
                                'image_path': "images/cow.png"})
        self.sound_bank.append({'sound_path': "sounds/90014__thfc140491__police-siren-perpignan_cropped.wav",
                                'image_path': "images/police.png"})
        self.sound_bank.append({'sound_path': "sounds/84111__benboncan__wind-on-door-short_cropped.wav",
                                'image_path': "images/wind.png"})

        self.init_ui()

    def init_ui(self):
        self.init_player()
        self.sound_button_group = ImageOptionButtonGroup()

        # Create widgets
        self.sounds_buttons = []
        for i, sound in enumerate(self.sound_bank):
            # It is important that the id passed to the ImageOptionButton constructor matches the index of the sound
            # in the sound_bank list, since it will be used to update the waveform display upon selection
            self.sounds_buttons.append(ImageOptionButton(i, sound['image_path']))
            self.sounds_buttons[-1].resize_image(150, 150)
            self.sounds_buttons[-1].selected.connect(self.selected_sound_action)
            self.sound_button_group.add_image_button(self.sounds_buttons[-1])

        self.selected_sound_display = WaveformDisplay()
        selected_sound_play_button = ImageButton("images/play2.png")
        selected_sound_play_button.resize_image(100, 100)
        selected_sound_play_button.clicked.connect(self.play_selected_sound)

        # Create layouts
        vertical_layout = QVBoxLayout()
        sounds_buttons_layout = QGridLayout()
        selected_sound_playback_layout = QHBoxLayout()

        # Setup vertical layout
        self.setLayout(vertical_layout)
        vertical_layout.addLayout(sounds_buttons_layout)
        vertical_layout.addStretch()
        vertical_layout.addLayout(selected_sound_playback_layout)

        # Setup grid of sounds
        positions = [(i, j) for i in range(1) for j in range(4)]
        for pos, sound_button in zip(positions, self.sounds_buttons):
            sounds_buttons_layout.addWidget(sound_button, pos[0], pos[1], Qt.AlignCenter)

        # Setup
        selected_sound_playback_layout.addWidget(selected_sound_play_button)
        selected_sound_playback_layout.addWidget(self.selected_sound_display)

        self.sounds_buttons[0].select()

    def init_player(self):
        self.player = QSoundEffect()
        self.player.setVolume(1)
        self.player.playingChanged.connect(self.play_selected_sound)

    @pyqtSlot()
    def selected_sound_action(self):
        # Update waveform display
        sound_path = self.sound_bank[self.sender().id]['sound_path']
        self.selected_sound_display.load_audio(sound_path)

    @pyqtSlot()
    def play_selected_sound(self):
        sound_path = self.sound_bank[self.sound_button_group.get_id_selected()]['sound_path']
        self.player.setSource(QUrl.fromLocalFile(sound_path))
        self.player.play()

    def report(self):
        print("Button #", self.sound_button_group.get_id_selected(), "is selected")
