#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET
import cerberus
import schema
import os

PATH = os.getcwd() + os.sep

OSM_PATH = "MAP" + os.sep + "Springfield_Illinois.osm"
streetNamesAndAbbreviationsPath = PATH + os.sep + "streetSuffixesAndAbbreviations.csv"
CSV_OUTPUT_PATH = PATH + os.sep + "csv_output" + os.sep

NODES_PATH = CSV_OUTPUT_PATH + "nodes.csv"
NODE_TAGS_PATH = CSV_OUTPUT_PATH + "nodes_tags.csv"
WAYS_PATH = CSV_OUTPUT_PATH + "ways.csv"
WAY_NODES_PATH = CSV_OUTPUT_PATH + "ways_nodes.csv"
WAY_TAGS_PATH = CSV_OUTPUT_PATH + "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']


k = 1

streetNamesAndAbbreviations = {}
with open(streetNamesAndAbbreviationsPath, 'r') as f:
    reader = csv.DictReader(f)
    for i in reader:
        keyValueTpl = tuple(i['primarySuffix;abbreviation'].split(";"))
        streetNamesAndAbbreviations[keyValueTpl[1]] = keyValueTpl[0]
    
