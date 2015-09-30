#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from geomate.geocoderAPI.base import BaseGeocoder
except:
    from .geocoderAPI.base import BaseGeocoder

from binascii import a2b_base64, b2a_base64
from pickle import dumps, loads
import sqlite3
import json
import sys

if sys.version_info[0] == 3:
    _str_type = str
else:
    _str_type = basestring
PICKLE_PROTOCOL = 2

def stringlize_address(address):
    """Convert string address or tuple coordinate to string.
    """
    if isinstance(address, _str_type):
        return address
    elif isinstance(address, tuple):
        if isinstance(address[0], float) and isinstance(address[1], float):
            return b2a_base64(dumps(address, protocol=PICKLE_PROTOCOL))\
                .decode("utf-8")
    
    raise TypeError("%s is not a valid input. " % repr(address))

def recover_address(address):
    """Recover string address from string address or tuple coordinate.
    """
    try:
        return loads(a2b_base64(address.encode("utf-8")))
    except:
        return address

class BatchGeocoder(object):
    """Geocoding Batch process engine.
    
    :param geocoder: A Geocoder client instance.
    :param db_file: the absolute path to the sqlite database file.
    """
    _table_name = "geo_result"
    _columns = ["address", "json"]
    _create_table_sql = ("CREATE TABLE geo_result " 
                         "(address TEXT PRIMARY KEY, json BLOB)")
    
    def __init__(self, geocoder, db_file):
        if not isinstance(geocoder, BaseGeocoder):
            raise TypeError(
                "%s is not a geomate.geocoder.base.BaseGeocoder "
                "type." % repr(geocoder))
            
        self.geocoder = geocoder
        self.connect = sqlite3.connect(db_file)
        self.connect.text_factory = str
        self.cursor = self.connect.cursor()
        
        # create table
        try:
            self.cursor.execute(BatchGeocoder._create_table_sql)
        except:
            pass
        
    def process(self, address_list):
        """Batch process list of address or coordinate tuple.
        """
        # exam input
        todo = set()
        for address in address_list:
            todo.add(stringlize_address(address))
        
        # insert data
        already_have = {record[0] for record in self.cursor.execute(
            "SELECT address FROM geo_result")}
        
        for address in todo.difference(already_have):
            self.cursor.execute(
                "INSERT INTO geo_result (address) VALUES (?)", (address,))
            
        self.connect.commit()
        
        # perform geocode
        for address, in list(self.cursor.execute(
            "SELECT address FROM geo_result WHERE json IS NULL")):
            input_ = recover_address(address)
            if isinstance(input_, str):
                res = self.geocoder.geocode(input_)
            else:
                res = self.geocoder.reverse(input_)
                
            if res:
                self.cursor.execute(
                    "REPLACE INTO geo_result (address, json) VALUES (?,?)", 
                    (address, json.dumps(res)))
                self.connect.commit()

    def lookup(self, address):
        """Return geocoded dict record of the address.
        """
        cursor = self.cursor.execute(
            "SELECT json FROM geo_result WHERE address == '%s'" % stringlize_address(address))
        return cursor.fetchone()


if __name__ == "__main__":
    from geomate.geocoder.google import GoogleGeocoder
    import unittest
    
    class StringLizeAddressUnittest(unittest.TestCase):
        def test_all(self):
            input_ = (38.860, -77.062)
            expect_ = "gAJHQENuFHrhR65HwFNEOVgQYk6GcQAu\n"
            s = stringlize_address(input_)
            origin = recover_address(s)
            
            self.assertAlmostEqual(input_[0], origin[0], 0.001)
            self.assertAlmostEqual(input_[1], origin[1], 0.001)

    unittest.main()