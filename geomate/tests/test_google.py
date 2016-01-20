#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint as ppt

import geomate
from geomate.tests import GOOGLE_API_KEYS

def test():
    api_keys = GOOGLE_API_KEYS[:3]
    googlegeocoder = geomate.GoogleGeocoder(api_keys=api_keys)
    googlegeocoder.check_usable()
     
    ppt(googlegeocoder.geocode("1400 S Joyce St"))
    ppt(googlegeocoder.reverse((38.860, -77.066)))
    
if __name__ == "__main__":
    test()