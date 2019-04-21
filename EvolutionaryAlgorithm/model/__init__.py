#!/usr/bin/python2.7
import logging

from .demand import Demand, DemandPath
from .link import Link
from .network import Network

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
