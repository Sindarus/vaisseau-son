#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-07-05

Reference for style conventions : https://www.python.org/dev/peps/pep-0008
"""
import _mysql
import os

from Config import Config


class SoundDBConnector:

    def __init__(self):
        self.db = _mysql.connect(
            host=Config.DB_ADDR,
            user=Config.DB_USER,
            passwd=self.get_db_passwd(),
            db=Config.SOUND_DB_NAME
        )

    def get_db_passwd(self):
        """Helper function to retrieve the database password following the configured method.

        :return: The password as a string
        """
        if Config.DB_PASSWD_GET_METHOD == "envvar":
            db_passwd = os.getenv(Config.DB_PASSWD_ENV_VAR_NAME)
            if db_passwd is None:
                raise (BaseException("Could not get database password from " + str(Config.DB_PASSWD_ENV_VAR_NAME) +
                                     " environment variable"))
            else:
                return db_passwd
        elif Config.DB_PASSWD_GET_METHOD == "config":
            return Config.DB_PASSWD
        else:
            raise(BaseException("Unknown DB_PASSWD_GET_METHOD value : \"" + str(Config.DB_PASSWD_GET_METHOD) + "\""))

    def add_sound(self, path, label, submitted, datetime_, duration):
        insert_query = 'INSERT INTO sounds VALUES (0,"%s","%s",%s,"%s",%s);' %\
                       (path, label, int(submitted), datetime_.isoformat(), duration)
        self.db.query(insert_query)
