#!/usr/bin/python2.7

import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

from .parser import read_file, print_values
