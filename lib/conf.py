import configparser

def get_config():
    config = configparser.ConfigParser()
    config.read('./conf/conf.ini')
    return config
