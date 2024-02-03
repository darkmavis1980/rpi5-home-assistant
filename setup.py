#!/usr/bin/env python

import os.path

import configparser

filePath = './conf/conf.ini'

def createConfig():
    config = configparser.ConfigParser()

    host = input('Please enter host: (defaults to localhost)').strip() or 'localhost'
    username = input('Please enter username:').strip() or ''
    password = input('Please enter password:').strip() or ''
    dbName = input('Please enter db name:').strip() or ''
    port = input('Please enter port: (defaults to 3306)').strip() or '3306'

    config.add_section('DATABASE')
    config.set('DATABASE', 'HOST', host)
    config.set('DATABASE', 'USERNAME', username)
    config.set('DATABASE', 'PASSWORD', password)
    config.set('DATABASE', 'DB', dbName)
    config.set('DATABASE', 'PORT', port)

    with open(filePath, 'w') as configfile:
        config.write(configfile)

if __name__ == "__main__":
    if (os.path.isfile(filePath) is False):
        print('Creating configuration file')
        createConfig()
    else:
        print('File already exists')