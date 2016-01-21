#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
About Google Map Geocoding API: 
https://developers.google.com/maps/documentation/geocoding/intro

How to get API Key:
https://developers.google.com/maps/documentation/geocoding/get-api-key
"""

from __future__ import print_function

import time
import logging

try:
    from geomate.geocoderAPI.base import BaseGeocoder
    from geomate.logger import baselogger
except:
    from .base import BaseGeocoder
    from ..logger import baselogger

from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderQuotaExceeded

class GoogleGeocoder(BaseGeocoder):
    """Simple Google V3 Geocoder API client.
    
    How to get API key: https://developers.google.com/maps/documentation/geocoding/get-api-key
    """
    def __init__(self, api_keys, sleeptime=0.1, logger=None):
        self.client_pool = dict()
        for key in api_keys:
            self.client_pool[key] = GoogleV3(key)
        
        self.api_keys = api_keys[::-1]
        
        self.sleeptime = sleeptime 
        
        if isinstance(logger, logging.Logger):
            self.logger = logger
        else:
            self.logger = baselogger
    
    def set_sleeptime(self, sleeptime):
        """Set sleeptime between two API call (in seconds.)
        """
        self.sleeptime = sleeptime

    def check_usable(self):
        """Exam if all API keys are usable. It spends 1 quota for each API keys 
        to perform this check.
        """
        self.logger.info("Checking API Key usability...")
        
        input_ = "1600 Pennsylvania Ave NW, Washington, DC 20500" # white house
        expect_ = "1600 Pennsylvania Ave NW, Washington, DC 20500, USA"
        
        bad_keys = list()
        for key in self.api_keys:
            time.sleep(1.0)
            try:
                geocoder = self.client_pool[key]
                location = geocoder.geocode(input_)
                formatted_address = location.raw["formatted_address"]
                if expect_ not in formatted_address:
                    raise Exception("Output is %r doens't match %r!" % 
                        (formatted_address, expect_))
            except Exception as e:
                self.logger.info(e)
                bad_keys.append(key)
                
        if len(self.api_keys) == 0:
            self.logger.info("There's no available API key.")
        elif len(bad_keys) == 0:
            self.logger.info("All API keys are usable.")
        else:
            self.logger.info("These keys are not available:")
            for key in bad_keys:
                self.logger.info(key)

    def geocode(self, address, exactly_one=True):
        """Return geocoded dict data by address string.
        """
        time.sleep(self.sleeptime)
        key = self.take_one_key()
        client = self.client_pool[key]
        try:
            locations = client.geocode(address, exactly_one=exactly_one)
            if exactly_one:
                result = locations.raw 
                self.logger.info("Successful to geocode %r" % address)
                return result
            else:
                result = [loc.raw for loc in locations]
                self.logger.info("Successful to geocode %r" % address)
                return result
        except GeocoderQuotaExceeded: # reach the maximum quota
            self.remove_one_key(key)
            return self.geocode(address) # try again with new key
        except Exception as e: # other error, return None
            self.logger.info("Failed to geocode %r, Error: %s" % (address, e))
            return None

    def reverse(self, address, exactly_one=True):
        """Do reverse lookup by latitude and longitude tuple, return dict data.
        """
        time.sleep(self.sleeptime)
        key = self.take_one_key()
        client = self.client_pool[key]
        try:
            lat, lng = address
            locations = client.reverse((lat, lng), exactly_one=exactly_one)
            if exactly_one:
                result = locations.raw
                self.logger.info("Successful to geocode %r" % address)
                return result
            else:
                result = [loc.raw for loc in locations]
                self.logger.info("Successful to geocode %r" % address)
                return result
        except GeocoderQuotaExceeded: # reach the maximum quota
            self.api.remove_one(key)
            return self.reverse((lat, lng), exactly_one=exactly_one) # try again with new key
        except Exception as e: # other error, return None
            self.logger.info("Failed to reverse geocode %r, Error: %s" % (address, e))
            return None