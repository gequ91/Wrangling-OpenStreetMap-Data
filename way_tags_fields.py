#!/usr/bin/env python
# -*- coding: utf-8 -*-

import settings
import re

# Every element goes through a special cleaning function based on it's tagKey - if there is no cleaning function for a tagkey, the tagValue will be returned as is
def cleanWayTag(elementId, tagKey, tagType, tagValue): 
    cleanFunction = "clean" + (tagKey[0].upper() + tagKey[1:]) if tagKey != None and tagKey != "" else "TagKeyError"
    if cleanFunction in globals().iterkeys():
        return globals()[cleanFunction](elementId, tagKey, tagType, tagValue )
    elif cleanFunction == "TagKeyError":
        raise KeyError("TagKeyError occured - no Tag key found, check element")
    else:     
        return tagValue

def cleanPhone(elementId, tagKey, tagType, tagValue):
    # As for the cleaning of phone numbers I will use the E.164 phone number formatting recommended here: https://support.twilio.com/hc/en-us/articles/223183008-Formatting-International-Phone-Numbers
    tagValue = re.sub("[^0-9]+", "", tagValue) # First we clean the phone number of any non-digit characters 
    if tagValue.startswith('1'):
        tagValue = "+" + tagValue 
    elif tagValue.startswith('217'):
        tagValue = "+1" + tagValue
    else:
        tagValue = "Phone number is not a local one " + tagValue
    return tagValue
    
    
def cleanMaxspeed(elementId, tagKey, tagType, tagValue):
    # It is better to have the speedlimit including the unit in the tagValue - as the United States uses miles, we can assume that every speed limit is denoted in miles.
    if 'mph' not in tagValue:
        tagValue = tagValue + ' mph'
    return tagValue

def cleanMinspeed(elementId, tagKey, tagType, tagValue):
    # Same procedure for Minspeed as for Maxspeed
    return cleanMaxspeed(elementId, tagKey, tagType, tagValue ) 

def cleanCity(elementId, tagKey, tagType, tagValue):
    if tagValue == ", Springfield":
        tagValue = "Springfield" 
    return tagValue

def cleanFence_type(elementId, tagKey, tagType, tagValue):
    # According to https://wiki.openstreetmap.org/wiki/Key:fence_type - "chain" shall no longer be used
    if tagValue == "chain": 
        tagValue = "chain_link" 
    return tagValue    

def cleanCounty(elementId, tagKey, tagType, tagValue):
    # All other county values are followed by their state 
    if tagValue == "Sangamon": 
        tagValue = "Sangamon, IL"
    return tagValue    

def cleanCreated(elementId, tagKey, tagType, tagValue):
    # Date format should by mm/dd/yyyy
    if tagValue == "03.12.2008": 
        tagValue = "12/03/2008"
    return tagValue    

def cleanState(elementId, tagKey, tagType, tagValue):
    # State is in all but one case 'IL' instead of 'Illinois' -> change to 'IL'
    if tagValue == "Illinois": 
        tagValue = "IL"
    return tagValue    
    
def cleanName(elementId, tagKey, tagType, tagValue):
    return cleanStreet(elementId, tagKey, tagType, tagValue )

def cleanStreet(elementId, tagKey, tagType, tagValue):
    if any(("Dr.", "Blvd." in tagValue)):
        tagValue = tagValue.replace("Dr.", "").replace("Blvd.", "")
        
    tagValueAsList = tagValue.split(" ")
    
    if any([x.lower() in [y.lower() for y in settings.streetNamesAndAbbreviations.iterkeys()] for x in tagValueAsList]): # check if street suffix is in prepared dictionary
        # if so - translate it to the primary suffix
        for subString in tagValueAsList:
            if subString.lower() in [y.lower() for y in settings.streetNamesAndAbbreviations.iterkeys()]:
                replacement = settings.streetNamesAndAbbreviations[subString.upper()]
                replacement = replacement[0] + replacement[1:].lower()
                tagValueAsList[tagValueAsList.index(subString)] = replacement
                
    tagValue = " ".join(tagValueAsList)
    return tagValue
    
    

