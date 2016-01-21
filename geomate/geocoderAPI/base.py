#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
All Geocoder class inherit from BaseGeocoder must have the following methods:

- ``geocode(str_address)``
- ``reverse(tuple_coordinate_lat_lng)`` 
"""
import random

class APIError(Exception):
    """API related error.
    """

class BaseGeocoder(object):
    """Geocoder base class.
    
    take_one_key randomly return a api key.
    if GeocoderQuotaExceeded been raised, remove the api key from pool    
    """    
    def take_one_key(self):
        try:
            return random.choice(self.api_keys)
        except IndexError:
            raise APIError("Run out of all API keys")
        
    def remove_one_key(self, key):
        try:
            self.api_keys.remove(key)
        except ValueError:
            raise APIError("Run out of all API keys")