#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import random
import sqlite3
import logging

try:
    from geomate.geocoderAPI.base import BaseGeocoder
except ImportError:
    from .geocoderAPI.base import BaseGeocoder

if sys.version_info[0] == 3:
    _str_type = str
else:
    _str_type = basestring

def stringlize_address(address):
    """Convert string address or tuple coordinate to string.
    """
    try:
        return json.dumps(address)
    except:
        raise TypeError("%s is not a valid input. " % repr(address))

def recover_address(address):
    """Recover string address from string address or tuple coordinate.
    """
    return json.loads(address)

class BatchGeocoder(object):
    """Geocoding Batch process engine.
    
    :param geocoder: A Geocoder client instance.
    :param db_file: the absolute path to the sqlite database file.
    """
    _table_name = "geo_result"
    _columns = ["address", "json"]
    _create_table_sql = ("CREATE TABLE geo_result " 
                         "(address TEXT PRIMARY KEY, json TEXT)")
    
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
        
    def add_addresses(self, address_list):
        """Put new todo address into database, but not geocode yet.
        """
        address_to_do = set()
        for address in address_list:
            address_to_do.add(stringlize_address(address))

        address_in_db = {record[0] for record in self.cursor.execute(
            "SELECT address FROM geo_result")}
        
        for address in address_to_do.difference(address_in_db):
            self.cursor.execute(
                "INSERT INTO geo_result (address) VALUES (?)", (address,))
            
        self.connect.commit()
        return address_to_do

    def batch_geocode(self, address_list):
        """Batch process list of address or coordinate tuple.
        """
        for address in address_list:
            recovered_address = recover_address(address)
            if isinstance(recovered_address, _str_type):
                res = self.geocoder.geocode(recovered_address)
            else:
                res = self.geocoder.reverse(recovered_address)
                
            if res:
                self.cursor.execute(
                    "REPLACE INTO geo_result (address, json) VALUES (?,?)", 
                    (address, json.dumps(res)))
                self.connect.commit()
    
    # Work logic
    def process_this(self, address_list, shuffle=False):
        """geocode this address list.
        """
        address_to_do = self.add_addresses(address_list)
        
        address_notdone = {record[0] for record in self.cursor.execute(
            "SELECT address FROM geo_result WHERE json IS NULL")}
        
        address_to_do = set.intersection(address_to_do, address_notdone)
        if shuffle:
            address_to_do = list(address_to_do)
            random.shuffle(address_to_do)
        
        self.geocoder.logger.info("Got %s addresses to work on..." % len(address_to_do))
        self.batch_geocode(address_to_do)
        self.geocoder.logger.info("Work complete!")
        
    def process_all(self, shuffle=False):
        """geocode everything haven't done in database.
        """
        address_notdone = {record[0] for record in self.cursor.execute(
            "SELECT address FROM geo_result WHERE json IS NULL")}

        if shuffle:
            address_notdone = list(address_notdone)
            random.shuffle(address_notdone)
        
        self.geocoder.logger.info("Got %s addresses to work on..." % len(address_to_do))
        self.batch_geocode(address_to_do)
        self.geocoder.logger.info("Work complete!")

    def lookup(self, address):
        """Return geocoded dict record of the address.
        """
        cursor = self.cursor.execute(
            "SELECT json FROM geo_result WHERE address = '%s'" % stringlize_address(address))
        res = cursor.fetchall()
        if len(res) == 1:
            return json.loads(res[0][0])
        else:
            return None

if __name__ == "__main__":
    import unittest
    
    class StringLizeAddressUnittest(unittest.TestCase):
        def test_all(self):
            origin_address = "675 15th St NW Washington, DC 20005"
            stringlized_address = stringlize_address(origin_address)
            recovered_address = recover_address(stringlized_address)
            self.assertEqual(origin_address, recovered_address)
            
            origin_address = (38.860, -77.062)
            stringlized_address = stringlize_address(origin_address)
            recovered_address = recover_address(stringlized_address)
            
            self.assertAlmostEqual(origin_address[0], recovered_address[0], 0.001)
            self.assertAlmostEqual(origin_address[1], recovered_address[1], 0.001)

    unittest.main()