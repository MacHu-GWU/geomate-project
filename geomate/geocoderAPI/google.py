#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
About Google Map Geocoding API: 
https://developers.google.com/maps/documentation/geocoding/intro
"""

from __future__ import print_function

try:
    from geomate.geocoder.base import BaseGeocoder
except:
    from .base import BaseGeocoder

from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderQuotaExceeded
import time

class GoogleGeocoder(BaseGeocoder):
    def __init__(self, api_keys, sleeptime=0.1):
        self.client_pool = dict()
        for key in api_keys:
            self.client_pool[key] = GoogleV3(key)
        
        self.api_keys = api_keys[::-1]
        
        self.sleeptime = sleeptime 
    
    def set_sleeptime(self, sleeptime):
        """Set sleeptime between two API call (in seconds.)
        """
        self.sleeptime = sleeptime

    def check_usable(self):
        """Exam if all API keys are usable. It spends 1 quota for each API keys 
        to perform this check.
        """
        input_ = "1600 Pennsylvania Ave NW, Washington, DC 20500" # white house
        expect_ = "1600 Pennsylvania Ave NW, Washington, DC 20500, USA"
        
        bad_keys = list()
        for key in self.api_keys:
            time.sleep(self.sleeptime)
            try:
                geocoder = self.client_pool[key]
                location = geocoder.geocode(input_)
                if location.raw["formatted_address"] != expect_:
                    raise Excpetion("Output doens't match `%s`!" % expect_)
            except Exception as e:
                print(e)
                bad_keys.append(key)
        
        if len(bad_keys) == 0:
            print("All API keys are usable")
        else:
            print("%s are not usable" % bad_keys)

    def geocode(self, address, exactly_one=True):
        """Return geocoded dict data by address string.
        """
        time.sleep(self.sleeptime)
        key = self.take_one_key()
        client = self.client_pool[key]
        try:
            locations = client.geocode(address, exactly_one=exactly_one)
            if exactly_one:
                return locations.raw
            else:
                return [loc.raw for loc in locations]
        except GeocoderQuotaExceeded: # reach the maximum quota
            self.remove_one_key()
            return self.geocode(address) # try again with new key
        except Exception as e: # other error, return None
            print(e)
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
                return locations.raw
            else:
                return [loc.raw for loc in locations]
        except GeocoderQuotaExceeded: # reach the maximum quota
            self.api.remove_one()
            return self.reverse((lat, lng)) # try again with new key
        except Exception as e: # other error, return None
            print(e)
            return None

if __name__ == "__main__":
    from pprint import pprint as ppt
    api_keys = [
        "AIzaSyAuzs8xdbysdYZO1wNV3vVw1AdzbL_Dnpk", # sanhe
    ]
    
    googlegeocoder = GoogleGeocoder(api_keys=api_keys)
    print(isinstance(googlegeocoder, BaseGeocoder))
    googlegeocoder.check_usable()
    ppt(googlegeocoder.geocode("1400 S Joyce St"))
    ppt(googlegeocoder.reverse(38.860, -77.066))
    