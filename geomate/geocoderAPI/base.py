#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
All Geocoder class inherit from BaseGeocoder must have the following methods:

- ``geocode(str_address)``
- ``reverse(tuple_coordinate_lat_lng)`` 
"""

class APIError(Exception):
    """API related error.
    """

class BaseGeocoder(object):
    """Geocoder base class.
    """    
    def take_one_key(self):
        try:
            return self.api_keys[-1]
        except IndexError:
            raise APIError("Run out of all API keys")
        
    def remove_one_key(self):
        try:
            self.api_keys.pop()
        except IndexError:
            raise APIError("Run out of all API keys")