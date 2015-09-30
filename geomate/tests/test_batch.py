#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import geomate
import json

class BatchGeocoderUnittest(unittest.TestCase):
    def test_all(self):
        api_keys = [
            "AIzaSyAuzs8xdbysdYZO1wNV3vVw1AdzbL_Dnpk", # sanhe
            "AIzaSyBfgV3y5z_od63NdoTSgu9wgEdg5D_sjnk", # rich
            "AIzaSyDsaepgzV7qoczqTW7P2fMmvigxnzg-ZdE", # meng yan
            "AIzaSyBqgiVid6V2xPZoADmv7dobIfvbhvGhEZA", # zhang tao
            "AIzaSyBtbvGbyAwiywSdsk8-okThcN3q515GDZQ", # jack
            "AIzaSyC5XmaneaaRYLr4H0x7HMRoFPgjW9xcu2w", # fenhan
            "AIzaSyDgM5xmKIjS_nooN_TBRLxrFDypVyON9bU", # Amina
            "AIzaSyCl95-wDqhxM1CtUzXjvirsAXCU_c1ihu8", # Ryan    
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