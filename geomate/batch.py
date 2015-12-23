#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from geomate.geocoderAPI.base import BaseGeocoder
except:
    from .geocoderAPI.base import BaseGeocoder
import sqlite3
import json
import sys

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

    def lookup(self, address):
        """Return geocoded dict record of the address.
        """
        cursor = self.cursor.execute(
            "SELECT json FROM geo_result WHERE address = '%s'" % stringlize_address(address))
        res = cursor.fetchall()
        if len(res) == 1:
            return json.loads(res[0][1])
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