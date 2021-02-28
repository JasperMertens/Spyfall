import configparser

def loadConfig ():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config
