#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .batch import BatchGeocoder
from .geocoderAPI.google import GoogleGeocoder 

__version__ = "0.0.3"
__short_description__ = ("Batch google geocoding tool. Automatically handle "
                         "API key, save result to disk and manage your todo list.")