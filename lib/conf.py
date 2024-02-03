import configparser

def getConfig():
    config = configparser.ConfigParser()
    config.read('./conf/conf.ini')
    return config
