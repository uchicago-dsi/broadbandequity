"""This module helps other data pipeline scripts access and read the config text file."""

import configparser
import os

config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), '../config.ini')
config.read(config_path)