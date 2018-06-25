# -*- coding: utf-8 -*-
"""
Created on Wed Dec 06 17:00:31 2017

@author: archa
"""

"""
Your task in this exercise has the following steps:

- audit the OSMFILE and inspect street names to be changed.
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "C:\\Users\\archa\\Nanodegree\\Data wrangling\\map.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "Way", "Terrace", "Allies", "Extension", "Automotive"]


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name) #search for last word in street name
    if m:
        street_type = m.group()
        if street_type not in expected: #Check if the street name are unexpected
            street_types[street_type].add(street_name) #Add to street_types if there are unexpected street names


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def is_postal_code(elem):
    return (elem.attrib['k'] == "addr:postcode")
    


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    postal_code = set()
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
                                       
                elif is_postal_code(tag):
                    postal_code.add(tag.attrib['v'])
                    
    osm_file.close()
    return street_types, postal_code



def test():
    st_types, postal_code = audit(OSMFILE)
    print st_types
    print postal_code
    

    
if __name__ == '__main__':
    test()