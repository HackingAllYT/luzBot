from crearImaxe import createImage
import configparser
import os

import logging

# Set up the logging
logging.basicConfig(filename='today.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info('Starting Bot...')

config = configparser.ConfigParser()
config.read('config.ini')

createImage(config['IMAGES']['TODAY'])

os.remove(config['IMAGES']['TOMORROW'])
logging.info(f'Succeed!')
