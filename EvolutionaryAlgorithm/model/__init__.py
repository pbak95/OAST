#!/usr/bin/python2.7
from .demand import Demand
from .link import Link

import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
