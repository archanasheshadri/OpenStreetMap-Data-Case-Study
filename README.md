# OpenStreetMap-Data-Case-Study

## Map Area
Pittsburgh,PA, United States

https://www.openstreetmap.org/export#map=12/40.4363/-79.9010
This map is where I live, so I’m more interested to see what database querying reveals and to know more about the city.

## Problems Encountered in the Map
After initially downloading a small sample size of the Pittsburgh area and running it against a provisional .py file, I noticed five main problems with the data, which I will discuss in the following order:
* Over Abbreviated street names (“S Tryon St Ste 105”)
* Inconsistent postal codes (“NC28226”, “28226­0783”, “28226”)
* “Incorrect” postal codes (Charlotte area zip codes all begin with “282” however a large portion of all documented zip codes were outside this region.)
* Second level “k” tags with the value "type"(which overwrites the element’s previously processed node[“type”]field).
Street names in second 
* level “k” tags pulled from Tiger GPS data and divided into segments, in the following format:
