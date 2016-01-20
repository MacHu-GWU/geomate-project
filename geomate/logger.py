#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

baselogger = logging.getLogger("geomate")

# Logging level
baselogger.setLevel(logging.DEBUG)

# Print screen level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
baselogger.addHandler(ch)

if __name__ == "__main__":
    baselogger.info("INFO")