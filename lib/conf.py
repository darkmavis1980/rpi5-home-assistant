"""Configparser module"""
import configparser

def get_config():
    """Get the configuration object"""
    config = configparser.ConfigParser()
    config.read('./conf/conf.ini')
    return config
