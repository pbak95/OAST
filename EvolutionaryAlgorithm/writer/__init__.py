#!/usr/bin/python2.7
import logging

from .writer import write_file

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
