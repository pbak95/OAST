#!/usr/bin/python2.7
from .demand import Demand, DemandPath
from .link import Link

import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
