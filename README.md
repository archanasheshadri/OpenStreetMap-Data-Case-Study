# OpenStreetMap Data Case Study Using SQL

**Student Name:** Archana Sheshadri
## Map Area
Pittsburgh,PA, United States

https://www.openstreetmap.org/export#map=12/40.4363/-79.9010 using overpass API (https://overpass-api.de/api/map?bbox=-80.0526,40.4093,-79.9358,40.4899)
This place is where I have moved recently, so I’m more interested to see to know more about the city I live.

## Problems Encountered in the Map

After initially downloading a small sample size of the Pittsburgh area and running it against a provisional .py file, I noticed three main problems with the data, which I will discuss in the following order:

* Abbreviated street names (“S Graham St”, "E Warrington Ave")
* Incorrect postal code (Pittsburgh area zip codes all begin with “15” - found that one of the postal codes was "14233" which has to be "15233")
* Street names in second level “k” tags pulled from Tiger GPS data and divided into segments, in the following format:
```xml
    <tag k="tiger:name_base" v="Sorrell"/>
    <tag k="tiger:name_type" v="St"/>
    <tag k="tiger:reviewed" v="no"/>
    <tag k="tiger:zip_left" v="15212"/>
    <tag k="tiger:zip_right" v="15212"/>
```

## Inspecting Street Names
Using inspect_street_name.py, I noticed there were few abbreviated street names and one inconsistent postal code. 

'St.': set(['Atwood St.']), 'Brdg': set(['Swindell Brdg']), 'St': set(['N Neville St', 'N Dithridge St', 'North Bellefield St', 'Winthrop St', 'S Graham St', 'South Dithridge St', 'Castleman St', 'South Craig St', 'South Craig Street;S Craig St', 'N Craig St', 'Henry St', 'S Craig St', 'Stanwix St']), 'Rd': set(['520 Unity Center Rd', 'Bayard Rd']), 'Av': set(['Center Av']), 'Blvd': set(['Fort Duquesne Blvd']), 'Ave': set(['Centre Ave', 'Forbes Ave', 'Fifth Ave', 'S Millvale Ave', '5th Ave', 'Arlington Ave', 'E Warrington Ave', 'Liberty Ave', 'Morewood Ave']), 'Ter': set(['Faber Ter', 'Colby Ter']), 'Pl': set(['Washington Pl']

'15213-2712', '15213-1500', '15213-1503', '15213-1502', '15213-1405', '15213-1400', '15213-2911', '15232-1418', '15260', '15233', '15213-1713', '15205', '15222', '15207', '15206', '15201', '15226', '15203', '15224', '15240', '15209', '15213-1704', '15213-1705', '15213-2608', '15232-1803', '15213-1530', '15232-1845', '15213-1763', '15232-2131', **'14233'**, '15220', '15213-4026', '15232-1421', '15213-3704', '15232-1419', '15213-2909', '15136', '15290', '15239', '15216', '15214', '15212', '15213', '15210', '15211', '15232-2106', '15232-1447', '15232', '15219', '15203-2275', '15213-1678', '15210-1845', '15213-1738'

## Updating street names and saving it into a csv file

To correct the street names, I iterated over each word since the street names were abbreviated at multiple postions in an address using preparing_for_database.py.

```python
def update_name(name, mapping):
    
    words = name.split()
    for word in range(len(words)):
        if words[word] in mapping:
            words[word] = mapping[words[word]]
            name = " ".join(words)
            
    return name  

def audit(element):
    if element.tag == "node" or element.tag == "way":
        for tag in element.iter("tag"):
            if is_street_name(tag):
                if audit_street_type(tag.attrib['v']):
                    street_name = tag.attrib['v']
                    better_name = update_name(street_name, mapping)
                    tag.attrib['v'] = better_name   
                         
    return 
```

The above code updates the abbreviated street name and updates the variable to write in the csv file.


After updating the street names and writing into csv files, the files were loaded into SQLite database.

## Count of data in each table

Getting to know the total number of records in each table.

```SQL
SELECT COUNT(*) FROM NODES;
```

```
426469
```


