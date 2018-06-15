## Wrangling OpenStreetMap Data
###### by Guido Quadt

##### Introduction


In this Udacity project we'll take a look at wrangling OpenStreetMap data with python.
The following steps are part of the project:
	- Choose any area of the world and export the respective OSM XML data
	- Tackle the encountered problems in the OSM data and clean the data
	- Export the clean data as a .csv or JSON file
	- Import the .csv or JSON into either a SQL database or MongoDB
	- Explore the dataset

Regarding the first step of the project, I decided that I would like to explore the data of my hometown Bonn - the former capital of Germany. 
Sadly after a long search, I just couldn't find any problem in the data - at least nothing that could easily identified as a problem. I had the same problem with some other areas or cities, like the Westerwald in Germany or the city of Reykjavík. With the first one I had the same problem like with Bonn. With Reykjavík it was even harder because of the local language that was used in the data.

So, as a Simpsons fan, I decided that I will simply take some town called Springfield in the United States - so I picked Springfield, Illinois. 
The map area can be found in the sources.txt.

#####Problems encountered in your map

After parsing the XML document and converting it to a csv file - because I went with SQL - I decided to take a look at the key/value combinations in Excel. This way I could identify most of the problems in the map.

The following problems were identified and cleaned in the map:

######Way tags:

**Problem** | **Solution**
----------------- | ----------
**Inconsistent formatting of phone numbers** | Applying the E.164 phone number formatting by using a regular expression to get only the digits, checking for the correct area code (217) and adding +1 as a prefix to the number.
**Missing unit in minimum and maximum speedlimit** | Adding the string ' mph' to the value
**Additional ', ' in city name in one case** | Replacing the value ', Springfield' with 'Springfield'
**Missing state abbreviation in county name** | Adding the string ', IL' to the value
**In all but one case the abbreviation 'IL' is used as state** | Change the value 'Illinois' to 'IL'
**The Fence_Type 'chain' is no longer in use** | Replace "chain" with 'chain_link'
**Date format in the 'created' variable not consistent** | Changing the date format for all to dd/mm/yyyy
**Varying street type abbreviations in both 'street' and 'name' variable** | Cleaned by using a .csv file containing abbreviations of street suffixes and their primary suffix. 

######Node tags:

**Problem** | **Solution**
----------------- | ----------
**Inconsitent formatting of phone numbers** | See above
**Missing unit in maximum speedlimit** | See above
**Missing state abbreviation in county name** | See above
**'Springfield' instead of 'IL' in state value** | Replace the value 'Springfield' with 'IL'
**One Postcode saved as '6270462704'** | Changed to '62704'

#####Overview of the Data

To get an overview of the data, let's first note that the size of the OSM file is about 118.6mb big. Which is quite large for a file that only consist of text. The other five files are of course smaller than the original file, since the only contain parts of it.

**File** | **Size**
--- | ---
**Springfield_Illinois.osm** | 118.6mb
**nodes** | 46.7mb
**nodes_tags** | 1.8mb
**ways** | 4.8mb
**ways_nodes** | 14.2mb
**ways_tags** | 5.7mb

Now let us look at some statistics describing the OSM file and the city of Springfield, Illinois. 

First let's take a look at the number of nodes by using the following SQL query:

```SQL
select count(*) as num from nodes
```

The result of which is: 527951 nodes.

Let's also look at the number of ways.

```SQL
select count(*) as num from nodes
```

The result of which is: 72556 ways.

When combining these two tables, we can see that we have 225 unique users contributing two the OSM map of Springfield. To clarify - we can only see the user that contributed to the node or way as the last person. We don't see all users contributing to a node or a way.

```SQL
select count(distinct users) from 
	(select distinct ways.user from ways 
    union all 
    select distinct nodes.user from nodes) as users;
```

It would be interesting to see how many nodes or ways each user contributed to.  Let's look at the top 10.
```SQL
select users, count(*)
from (select ways.user
	  from ways 
	  union all 
	  select nodes.user 
	  from nodes) 
	  as users
	  group by users
	  order by count desc
	  limit 10;
```

**User** | **Count**
---------|-----------
(salisburymistake)|505894
(Sundance)|37848
(TIGERcnl)|11649
(DrTriforce)|10709
(Preferred)|5038
(HubMiner)|4228
(maxerickson)|2337
(woodpeck_fixbot)|2328
(freebeer)|1756
(rusefkuma)|1665

As we can see the user salisburymistake contributed by far the most - with more than 84% of all nodes and ways - as the last person who edited the node/way. 

I'm also curious how active the users are. Let's see how long ago their oldest edit and their newest edit are. We are going to sort the output descending by the newest edit, to so how up-to-date the changes are.

```SQL
select usersAndTimestamp.user, min(usersAndTimestamp.timestamp) as minDate, max(usersAndTimestamp.timestamp) as maxDate
from (select ways.user, ways.timestamp
	from ways 
	union all 
	select nodes.user, nodes.timestamp
	from nodes)
	as usersAndTimestamp
	group by usersAndTimestamp.user
	order by maxDate desc
	limit 20;
```

**User** | **Oldest edit** | **Newest edit**
----- | ----- | -----
salisburymistake|2016-02-12T17:05:55Z|2018-04-16T21:27:39Z
DougPeterson|2018-04-12T22:27:34Z|2018-04-12T22:27:34Z
Polyglot|2018-04-10T16:17:39Z|2018-04-10T16:34:32Z
EdSS|2017-02-20T22:57:47Z|2018-04-08T15:15:56Z
DrTriforce|2017-12-01T14:04:09Z|2018-04-06T02:09:01Z
Brutus|2018-04-05T23:34:39Z|2018-04-05T23:34:40Z
rusefkuma|2018-03-30T07:22:24Z|2018-03-31T14:05:38Z
DoubleA|2018-03-26T17:01:42Z|2018-03-26T17:01:46Z
HubMiner|2014-08-29T21:22:27Z|2018-03-13T20:39:55Z
Autumn_Smith|2018-03-10T02:16:23Z|2018-03-10T02:29:06Z
jackmoore427|2018-03-09T16:29:48Z|2018-03-09T16:29:49Z
Brandify Tran|2018-03-08T19:46:42Z|2018-03-08T19:58:31Z
Balkdon|2018-02-26T21:53:35Z|2018-02-26T21:53:37Z
Stephen214|2018-02-19T21:33:30Z|2018-02-19T23:12:35Z
UIS Web Services|2014-10-31T17:24:30Z|2018-02-13T18:29:26Z
AbbyO12|2018-01-04T02:25:04Z|2018-02-12T19:44:19Z
teodorab_telenav|2017-08-28T09:22:23Z|2018-02-08T12:44:35Z
hofoen|2015-01-21T11:09:19Z|2018-02-07T11:08:26Z
snodnipper|2018-02-04T13:20:18Z|2018-02-04T13:20:18Z
DocDrea323|2018-01-31T02:27:46Z|2018-01-31T02:27:46Z

Seems like the other with the most edit is also the one how made the most recent change to the data. Also some other top 10 users are in the list - like DrTriForce and HubMiner.

Now let's take a look what the city of Springfield has to offer - starting with the amenities. 

```SQL
select nodes_tags.value, count(*)
from nodes_tags
where nodes_tags.key='amenity' or nodes_tags.key='amenity'
group by nodes_tags.value
order by count desc
```

**Cuisine** | **Count** 
----|----
bench |696
waste_basket |213
recycling |101
restaurant |70
post_box |68
waste_disposal |63
toilets |50
school |50
grave_yard |47
fast_food |41
fountain |38
shelter |36
bicycle_parking |33
place_of_worship |24
parking |22
bar |19
vending_machine |17
atm |15
drinking_water |12
car_wash |11
social_facility |11
fuel |11
pharmacy |10
bbq |9
compressed_air |9
cafe |8
bank |8
charging_station |8
post_office |8
police |7
fire_station |7
bicycle_repair_station |5
veterinary |4
community_centre |3
cinema |3
library |3
clock |3
music_venue |2
kindergarten |2
clinic |2
theatre |2
pub |2
university |1
bus_station |1
childcare |1
courthouse |1
prison |1
animal_boarding |1
townhall |1
waste_transfer_station |1
arts_centre |1
parking_entrance |1
studio |1
hospital |1
telephone |1
first_aid |1
public_bookcase |1
dentist |1
doctors |1
college |1
nightclub |1


As we can see Springfield has a lot to offer - 70 restaurants,  41 fast food restaurants, 19 bars, 8 cafes and even 3 cinemas. Also there is a university and exactly 50 schools in the area. What seems odd is the low number of dentists or doctors - I would guess, that not all of them are included in the map. 

No let's look what the local cuisine has to offer. 

```SQL
select nodes_tags.value, count(*)
from nodes_tags
where nodes_tags.key='cuisine'
group by nodes_tags.value
order by count desc
```

**Cuisine** | **Count** 
----|----
burger|14
sandwich|13
pizza|12
mexican|9
american|8
chinese|6
chicken|4
coffee_shop|4
regional|3
italian|3
breakfast|2
donut|2
japanese|2
ice_cream|2
yogurt|1
american;chicken;fish;grill;ice_cream;italian_pizza;mexican|1
asian|1
indian|1
mexican;tacos|1
sushi|1
thai|1

It seems like we do have a lot of american style restaurants which specialise on burgers, sandwiches and american food in general. There are also a lot of restaurants that offer mexican cuisine. Two restaurants seem to offer more than one type of food. 

#####Other ideas about the datasets

There is plenty room for improvement of the dataset - or OSM data in general. For example there could be agreements for formats of phone numbers or using ISO formats for countries. 
But also agreements on how colour is stored as value - as an example: We have some colours in the way tags stored in hex, but also some stored as a string like "light_gray" or "yellow". I would suggest to use the first one, since we don't know how to define "light_gray" or "yellow". 

Another thing that could be improved would be values, that store multiple values inside. Like in the cuisine example above - where we have some restaurant that sells american and mexican food as well as chicken, fish, grilled food, ice cream and italian pizza. A system like we have seen with the amenities - where the first amenity is stored in the key "amenity" and the second is stored in the key "amenity_1" would help analysing these values.

Last but not least it would help a lot to always put units to a string. Of course we can assume that speedlimits in the United States always use the unit miles per hour - but in some other countries we may not be sure about that. The same for weight, width or height.

Of course all of that would only be agreements, data that is stored by humans is always prone for errors. 

Regarding the cleaning of the data, we could look other types of dirty data. This cleaning procedure focused primary on the uniformity, validity and consistency of data. 
We could also look for accuracy - for example we could use all the addresses in the data and check if they really exist. We could also look for completeness in the data, like do all - for example - schools in the area have a representation in the dataset. But these two are very hard or at least time consuming to address. 

#####Sources
Link to the map area in OpenStreetMap:
https://www.openstreetmap.org/#map=11/39.7990/-89.5242

Street Name Suffixes according to US Postal Service:
https://pe.usps.com/text/pub28/28apc_002.htm

Key Descriptions OSM:
https://wiki.openstreetmap.org/wiki/Category:Key_descriptions

Key: "fence_type" - Value: "chain" no longer in use:
https://wiki.openstreetmap.org/wiki/Key:fence_type

Getting rid of blank lines in csv output:
https://stackoverflow.com/questions/8746908/why-does-csv-file-contain-a-blank-line-in-between-each-data-line-when-outputting

Calling a function by it's string name:
https://stackoverflow.com/questions/3061/calling-a-function-of-a-module-by-using-its-name-a-string

Phone number cleaning:
https://docs.python.org/3/howto/regex.html
https://stackoverflow.com/questions/22520932/python-remove-all-non-alphabet-chars-from-string
https://support.twilio.com/hc/en-us/articles/223183008-Formatting-International-Phone-Numbers