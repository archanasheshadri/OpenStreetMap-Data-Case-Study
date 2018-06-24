# OpenStreetMap Data Case Study Using SQL

**Student Name:** Archana Sheshadri
## Map Area
Pittsburgh,PA, United States

https://www.openstreetmap.org/export#map=12/40.4363/-79.9010
This place is where I live, so I’m more interested to see what database querying reveals to know more about the city I live.

## Problems Encountered in the Map

After initially downloading a small sample size of the Pittsburgh area and running it against a provisional .py file, I noticed four main problems with the data, which I will discuss in the following order:

* Abbreviated street names (“S Graham St”, "E Warrington Ave")
* Uncommon street names (“Colby Terrace”, “Federal Street Extension”, “Boulevard of the Allies”)
* Incorrect postal code (Pittsburgh area zip codes all begin with “15” - found that one of the postal codes was "14233" which has to be "15233")
* Street names in second level “k” tags pulled from Tiger GPS data and divided into segments, in the following format:
    <tag k="tiger:name_base" v="Sorrell"/>
    <tag k="tiger:name_type" v="St"/>
    <tag k="tiger:reviewed" v="no"/>
    <tag k="tiger:zip_left" v="15212"/>
    <tag k="tiger:zip_right" v="15212"/>
