# OpenStreetMap Data Case Study Using SQL

**Student Name:** Archana Sheshadri
## Map Area
Pittsburgh,PA, United States

https://www.openstreetmap.org/export#map=12/40.4363/-79.9010 using overpass API (https://overpass-api.de/api/map?bbox=-80.0526,40.4093,-79.9358,40.4899)
This place is where I have moved recently, so I’m more interested to see to know more about the city I live.

## Problems Encountered in the Map

After initially downloading a small sample size(sample_file.py) of the Pittsburgh area and running it against a inspect_street_names.py file, I noticed three main problems with the data, which I will discuss in the following order:

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
There were also many uncommon street names like 'Terrace' which had to be identified to consider it valid.

## Inspecting Street Names
Using inspect_street_name.py, I noticed there were few abbreviated street names and one inconsistent postal code. 
```
'St.': set(['Atwood St.']), 'Brdg': set(['Swindell Brdg']), 'St': set(['N Neville St', 'N Dithridge St', 'North Bellefield St', 'Winthrop St', 'S Graham St', 'South Dithridge St', 'Castleman St', 'South Craig St', 'South Craig Street;S Craig St', 'N Craig St', 'Henry St', 'S Craig St', 'Stanwix St']), 'Rd': set(['520 Unity Center Rd', 'Bayard Rd']), 'Av': set(['Center Av']), 'Blvd': set(['Fort Duquesne Blvd']), 'Ave': set(['Centre Ave', 'Forbes Ave', 'Fifth Ave', 'S Millvale Ave', '5th Ave', 'Arlington Ave', 'E Warrington Ave', 'Liberty Ave', 'Morewood Ave']), 'Ter': set(['Faber Ter', 'Colby Ter']), 'Pl': set(['Washington Pl']
```
```
'15213-2712', '15213-1500', '15213-1503', '15213-1502', '15213-1405', '15213-1400', '15213-2911', '15232-1418', '15260', '15233', '15213-1713', '15205', '15222', '15207', '15206', '15201', '15226', '15203', '15224', '15240', '15209', '15213-1704', '15213-1705', '15213-2608', '15232-1803', '15213-1530', '15232-1845', '15213-1763', '15232-2131', **'14233'**, '15220', '15213-4026', '15232-1421', '15213-3704', '15232-1419', '15213-2909', '15136', '15290', '15239', '15216', '15214', '15212', '15213', '15210', '15211', '15232-2106', '15232-1447', '15232', '15219', '15203-2275', '15213-1678', '15210-1845', '15213-1738'
```
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

## Check the changes done to the street names

Let's check if the street names are updated in the file. As mentioned above there were few street names which were abbreviated. To verify I query the database with an example 'N Dithridge St'. 
```SQL
select tags.value
FROM (select * from ways_tags
union all
select * from nodes_tags) tags
where tags.key = 'street' and
tags.value like '%Dithridge%';
```
```
"North Dithridge Street"
"North Dithridge Street"
"Dithridge Street"
"North Dithridge Street"
"Dithridge Street"
"Dithridge Street"
"Dithridge Street"
"South Dithridge Street"
"North Dithridge Street"
"North Dithridge Street"
"North Dithridge Street"
"North Dithridge Street"
"North Dithridge Street"
"North Dithridge Street"
"North Dithridge Street"
"North Dithridge Street"
"North Dithridge Street"
"North Dithridge Street"
"North Dithridge Street"
"North Dithridge Street"
"North Dithridge Street"
"North Dithridge Street"
"North Dithridge Street"
"North Dithridge Street"
"North Dithridge Street"
"North Dithridge Street"
"North Dithridge Street"
```
All the entries are updates with full street names.

## Count of postal codes

Let's see the top 10 postal codes for the city of Pittsburgh.

```SQL
select tags.value, count(*) as count
FROM (select * from ways_tags
union all
select * from nodes_tags) tags
where tags.key = 'postcode' 
group by tags.value
order by count desc
limit 10;
```
```
15214,2490
15216,1459
15203,509
15222,253
15213,162
15233,63
15232,60
15206,53
15219,49
15201,35
```

We can see that most of the postal codes are consistent, except for one mistake which I mentioned earlier. Also we must note that the Tiger GPS data is not accounted for in this query.

## Count of cities

Let's move on to know all the city names.

```SQL
SELECT tags.value, COUNT(*) as count 
FROM (SELECT * FROM nodes_tags 
UNION ALL 
SELECT * FROM ways_tags) tags
WHERE tags.key = 'city'
GROUP BY tags.value
ORDER BY count DESC;
```
```
Pittsburgh,3459
"Pittsburgh, PA",54
"McKees Rocks",16
Pittburgh,4
Pittsburg,3
"Stowe Twp",3
"Mt. Washington",1
Oakland,1
Pittsburh,1
pittsburgh,1
```

We can see the majority of the entries are from Pittsburgh city. Also we can see that there are typos and as a result there multiple entries for the same name Pittsburgh.

## File sizes
The below python code helps to find the file sizes:

```Python
print ('Main file:', os.path.getsize('C:\\Users\\archa\\Nanodegree\\Data wrangling\\map.osm'))
print ('Sample file:' ,os.path.getsize('C:\\Users\\archa\\Nanodegree\\Data wrangling\\sample.osm'))
print ('Nodes file:', os.path.getsize('C:\\Users\\archa\\Nanodegree\\Data wrangling\\nodes.csv'))
print ('Nodes_tags file:',os.path.getsize('C:\\Users\\archa\\Nanodegree\\Data wrangling\\nodes_tags.csv'))
print ('Ways file:',os.path.getsize('C:\\Users\\archa\\Nanodegree\\Data wrangling\\ways.csv'))
print ('Ways_tags file:',os.path.getsize('C:\\Users\\archa\\Nanodegree\\Data wrangling\\ways_tags.csv'))
print ('Ways_nodes file:',os.path.getsize('C:\\Users\\archa\\Nanodegree\\Data wrangling\\ways_nodes.csv'))
```
Below is the result in bytes

```
('Main file:', 102548744L)
('Sample file:', 10365308L)
('Nodes file:', 2538424L)
('Nodes_tags file:', 63858L)
('Ways file:', 350649L)
('Ways_tags file:', 409930L)
('Ways_nodes file:', 872715L)
```

## Numer of nodes and ways

```SQL
SELECT COUNT(*) FROM nodes;
```
426469

```SQL
SELECT COUNT(*) FROM ways;
```
79710

## Number of unique users

```SQL
SELECT COUNT(DISTINCT(uid))          
FROM (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways);
```
448


## Additional statistics

### Top 10 contributing users
```SQL
SELECT user, COUNT(*) as count
FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) 
GROUP BY user
ORDER BY count DESC
LIMIT 10; 
```

```
doktorpixel14_import,145917
GeoKitten_import,93042
cowdog,54528
Omnific,48934
tmb926,30876
GeoKitten,29214
abbafei,20189
Roadsguy,9961
mdroads,6788
wegavision,4472
```


### Top 10 amenities in Pittsburgh

```SQL
SELECT value, COUNT(*) as count
FROM nodes_tags
WHERE key='amenity'
GROUP BY value
ORDER BY count DESC
limit 10;
```

```
restaurant,151
place_of_worship,101
school,87
bench,63
waste_basket,62
bicycle_parking,54
library,52
post_box,50
fast_food,40
cafe,37
```

Restaurants seems to be the top amenity. Let's have a look at top 10 cusines.

```SQL
SELECT value, COUNT(*) as count
FROM nodes_tags
WHERE key='cuisine'
GROUP BY value
ORDER BY count DESC
limit 10;
```
```
pizza,15
coffee_shop,14
sandwich,12
american,8
italian,6
burger,5
mexican,5
chinese,4
asian,3
indian,3
```
We can see that Pizza is most available food.

### Popular tourism places

```SQL
SELECT tags.value, COUNT() as count
FROM (SELECT * FROM nodes_tags UNION ALL
SELECT * FROM ways_tags) tags
WHERE tags.key = 'tourism'
GROUP BY tags.value
ORDER BY count DESC;
```
```
hotel,38
artwork,19
museum,18
viewpoint,10
attraction,7
guest_house,2
hostel,2
picnic_site,2
theme_park,2
Botanical_garden,1
information,1
```

## Additional ideas
```SQL
SELECT COUNT(*) FROM nodes;
```
426469

```SQL
SELECT COUNT(*) FROM nodes_tags WHERE key='wheelchair';
```
58

When I look at the wheelchair accessibility for the nodes, its just 58 out of 426469. Also this information could be updated for the amenities, restaurants and other popular public places.

### Ideas for improvement of the dataset

* We can try to control typos and other irregular data by creating a filter for the information entered.
* We can restrict the users to type in wrong data by creating validating(incorporating some rules) steps while the data is being entered.

## Conclusion

Based on the analysis done to the data, I would say that the data for Pittsburgh was fairly clean. There could be more cleaning and validating done to the Tiger GPS data which is not covered in this analysis. 
The dataset contains very less amount of additional information such as amenities, tourist attractions, popular places and other useful interest. 
















