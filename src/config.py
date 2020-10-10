"""
Class to access config.
"""

import configparser


class Config:
    __conf = None

    @staticmethod
    def config():
        if Config.__conf is None:  # Read only once, lazy.
            Config.__conf = configparser.RawConfigParser()
            config_file_path = r'./leaderboard_config.txt'
            Config.__conf.read(config_file_path)
        return Config.__conf
