#!/usr/bin/python2.7

import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

from .writer import write_file
