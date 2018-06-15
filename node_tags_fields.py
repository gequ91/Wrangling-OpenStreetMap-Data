#!/usr/bin/env python
# -*- coding: utf-8 -*-

import way_tags_fields

# Every element goes through a special cleaning function based on it's tagKey - if there is no cleaning function for a tagkey, the tagValue will be returned as is
def cleanNodeTag(elementId, tagKey, tagType, tagValue ): 
    cleanFunction = "clean" + (tagKey[0].upper() + tagKey[1:]) if tagKey != None and tagKey != "" else "TagKeyError"
    if cleanFunction in globals().iterkeys():
        return globals()[cleanFunction](elementId, tagKey, tagType, tagValue )
    elif cleanFunction == "TagKeyError":
        raise KeyError("TagKeyError occured - no Tag key found, check element")
    else:     
        return tagValue   
    
    
def cleanPhone(elementId, tagKey, tagType, tagValue):
    # We'll use the same function for the correction of phone numbers for both way_tags and node_tags
    return way_tags_fields.cleanPhone(elementId, tagKey, tagType, tagValue)
    
def cleanMaxspeed(elementId, tagKey, tagType, tagValue):
    # We'll use the same function for the correction of speedlimit for both way_tags and node_tags
    return way_tags_fields.cleanMaxspeed(elementId, tagKey, tagType, tagValue)
    
def cleanStreet(elementId, tagKey, tagType, tagValue):
    # We'll use the same function for the correction of street names for both way_tags and node_tags
    return way_tags_fields.cleanStreet(elementId, tagKey, tagType, tagValue)    
    
def cleanCounty(elementId, tagKey, tagType, tagValue):
    # County values in way tags have the state appended to the county - so we will do the same here
    tagValue = tagValue + ", IL"
    return tagValue        

def cleanPostcode(elementId, tagKey, tagType, tagValue):
    # The postcode 6270462704 doesn't exist - we can assume that this is an error, because 62704 does.
    if tagValue == "6270462704": 
        tagValue = "62704"
    return tagValue    

def cleanState(elementId, tagKey, tagType, tagValue):
    # The state "Springfield" doesn't exist - it is therefore corrected to "IL".
    if tagValue == "Springfield": 
        tagValue = "IL"
    return tagValue        