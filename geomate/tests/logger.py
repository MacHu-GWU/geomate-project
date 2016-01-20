#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
wbhRuntimeForecasting logger

LEVEL:

CRITICAL    50
ERROR       40
WARNING     30
INFO        20
DEBUG       10
NOTSET      0
"""

import logging

logger = logging.getLogger("geomate")

# Logging level
logger.setLevel(logging.DEBUG)

# Print screen level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)

# File handler
fh = logging.FileHandler("geomate.log")

# Formatter
formatter = logging.Formatter("%(asctime)s;\t%(levelname)s;\t%(message)s;")
fh.setFormatter(formatter)
logger.addHandler(fh)

if __name__ == "__main__":
    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
    logger.critical("critical")