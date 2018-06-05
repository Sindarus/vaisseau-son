#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-25

Reference for style conventions : https://www.python.org/dev/peps/pep-0008
"""


class Config:
    SOUNDS = {
        "lion": {'sound_path': "sounds/232289__zglar__zombie-or-monster-or-lion-roar.wav",
                 'image_path': "images/lion.png",
                 'display_name': "un rugissement"},
        "cow": {'sound_path': "sounds/58277__benboncan__cow.wav",
                'image_path': "images/cow.png",
                'display_name': "un beuglement"},
        "police": {'sound_path': "sounds/90014__thfc140491__police-siren-perpignan_cropped.wav",
                   'image_path': "images/police.png",
                   'display_name': "un sifflement de vent"},
        "wind": {'sound_path': "sounds/84111__benboncan__wind-on-door-short_cropped.wav",
                 'image_path': "images/wind.png",
                 'display_name': "un sifflement de vent"}
    }
    DEBUG_FFMPEG = False

    # UI
    FULLSCREEN = False
    WINDOW_MODE_WIDTH = 1000
    WINDOW_MODE_HEIGHT = 1020
    SOUND_IMAGE_SIZE = 150
    PLAYBACK_BUTTON_ICON_SIZE = 100
    SOUND_IMAGES_COLUMNS = 4
    SOUND_IMAGES_ROWS = 1
    MAIN_RESULT_IMAGE_SIZE = 400
    EXTRA_RESULT_IMAGE_SIZE = 150
    NAV_ICON_SIZE = 75
    LITTLE_NAV_ICON_SIZE = 50
    NOTIFICATION_MESSAGES_TIMEOUT = 5000  # in msec
    IMAGE_BUTTON_HOLD_BORDER_WIDTH = 4

    # Waveform
    WAVEFORM_IMG_SIZE = "1500x270"
    WAVEFORM_DISPLAY_HEIGHT = 270
    WAVEFORM_DISPLAY_WAVE_COLOR = "3232c8"
    WAVEFORM_DISPLAY_BG_COLOR = "b3d0fc"
    WAVEFORM_DISPLAY_GRID_OPACITY = "0.4"
    # Colors
    LIGHT_LIGHT_BLUE = "#dae8fc"
    LIGHT_BLUE = "#b3d0fc"
    BLUE = "#3232c8"
    BORDER_BLUE = "#6c8ebf"
    VIVID_BLUE = "#008cff"
    FONT_COLOR = "#4d4d4d"

    # Text
    TITLE = "Atelier son"
    VALIDATE_BUTTON = "Envoyer"
    LOADING_TEXT = "L'IA analyse votre son, merci de patienter :)"
    CANCEL_IA_TEXT = "Annuler"
    RESULTS_GROUP_TEXT = "Résultats"
    BACK_ARROW_TEXT = "Retour"
    RELOAD_ICON_TEXT = "Tout recommencer"
    RESULT_ITEM_TEXT = "L'IA a reconnu %s\navec une certitude de %i%%"
    EXTRA_RESULT_ITEM_TEXT = "%i%%"
    WAVEFORM_DISPLAY_PLACEHOLDER_MSG = "Votre extrait sonore apparaitra ici après enregistrement"
    CURRENTLY_RECORDING_MSG = "Enregistrement en cour !"

    # Audio
    N_CHANNELS = 1
    SAMPLE_SIZE = 32  # in bits
    SAMPLE_RATE = 44100  # in hertz
    TOO_SHORT_THRESHOLD = 0.5  # minimum duration of a user recording. If shorter, it will not be taken into account
