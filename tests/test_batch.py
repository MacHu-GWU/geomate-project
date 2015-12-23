#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import geomate
import json

class BatchGeocoderUnittest(unittest.TestCase):
    def test_all(self):
        api_keys = [
            "AIzaSyAuzs8xdbysdYZO1wNV3vVw1AdzbL_Dnpk", # sanhe
        ]
        googlegeocoder = geomate.GoogleGeocoder(api_keys=api_keys)
        batch = geomate.BatchGeocoder(googlegeocoder, db_file="geocode.sqlite3")

        list_of_address = [
            "675 15th St NW Washington, DC 20005",
            "2317 Morgan Ln Dunn Loring, VA 22027",
            "1201 Rockville Pike Rockville, MD 20852",
            ]
        list_of_coordinates = [
            (39.085801, -77.084513),
            (38.872719, -77.306417),
            (38.902027, -77.053536),
            ]
        list_of_address = list_of_address + list_of_coordinates
        batch.process(list_of_address)
        
        for address in list_of_address:
            print(batch.lookup(address))
            
if __name__ == "__main__":
    unittest.main()