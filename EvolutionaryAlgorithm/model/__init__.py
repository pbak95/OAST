#!/usr/bin/python2.7
from .demand import Demand, DemandPath, DemandFlow, DemandPathFlow
from .link import Link, LinkLoad

import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
