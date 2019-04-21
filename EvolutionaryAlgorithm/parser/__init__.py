#!/usr/bin/python2.7
import logging

from .parser import read_file

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
