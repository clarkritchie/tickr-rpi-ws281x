#!/usr/bin/env python3

import logging, os
logging.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO').upper())
from singleton import Singleton

@Singleton
class Strand:

    def do_stuff(self, data):
        logging.debug("Send to LED lights: %s" % data)

    def __init__(self):
        logging.info("Setup LED light strand stuff here")