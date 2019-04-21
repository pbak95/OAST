#!/usr/bin/python2.7
import logging

from .network import Network
from .demand import Demand, DemandPath
from .link import Link

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
