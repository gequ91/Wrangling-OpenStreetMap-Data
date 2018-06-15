#!/usr/bin/env python
# -*- coding: utf-8 -*-

from settings import *
import node_fields
import node_tags_fields
import way_fields
import way_nodes_fields
import way_tags_fields

def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements

    # YOUR CODE HERE
    if element.tag == 'node':
        elementAttributesToDict(element, NODE_FIELDS, node_attribs)
        parseTags(element, tags)
        return {'node': node_attribs, 'node_tags': tags}
    elif element.tag == 'way':
        elementAttributesToDict(element, WAY_FIELDS, way_attribs)
        parseNds(element, way_nodes)
        parseTags(element, tags)        
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}


# ================================================== #
#               Helper Functions                     #
# ================================================== #

#def parseNds(element):
    #ndDict = [{"id": element.attrib["id"], "node_id": nd.attrib["ref"], "position": i} for i, nd in enumerate(element.iter("nd"))]

def parseNds(element, way_nodes):
    for i,nd in enumerate(element.iter("nd")):
        ndDict = {"id": element.attrib["id"], "node_id": nd.attrib["ref"], "position": i}          
        way_nodes.append(ndDict)


def parseTags(element, tags):
    for tag in element.iter("tag"):
        tagDict = {"id": element.attrib["id"], "key": "", "value": "", "type": ""}  
        key = tag.attrib["k"].split(":", 1)
        if PROBLEMCHARS.search(tag.attrib["k"]) == None:
            if len(key) == 1:
                tagDict["key"] = tag.attrib["k"]
                tagDict["type"] = "regular"
            elif len(key) == 2:
                tagDict["key"] = key[1]
                tagDict["type"] = key[0]
            if element.tag == "node":
                tagDict["value"] = node_tags_fields.cleanNodeTag(elementId = element.attrib["id"], tagKey = tagDict["key"], tagType = tagDict["type"], tagValue = tag.attrib["v"] )
            elif element.tag == "way":
                tagDict["value"] = way_tags_fields.cleanWayTag(elementId = element.attrib["id"], tagKey = tagDict["key"], tagType = tagDict["type"], tagValue = tag.attrib["v"] )
            tags.append(tagDict)

def elementAttributesToDict(element, attributes, dictionary):
    updateTuples = ((attribute,element.attrib[attribute]) for attribute in attributes)
    dictionary.update(updateTuples)

def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)

        raise Exception(message_string.format(field, error_string))


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS, lineterminator='\n') 	# lineterminator='\n' added to get rid of blank lines in csv output
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS, lineterminator='\n')
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS, lineterminator='\n')
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS, lineterminator='\n')
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS, lineterminator='\n')

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for i, element in enumerate(get_element(file_in, tags=('node', 'way'))):
            if i % k == 0:
                el = shape_element(element)
                if el:
                    if validate is True:
                        validate_element(el, validator)
        
                    if element.tag == 'node':
                        nodes_writer.writerow(el['node'])
                        node_tags_writer.writerows(el['node_tags'])
                    elif element.tag == 'way':
                        ways_writer.writerow(el['way'])
                        way_nodes_writer.writerows(el['way_nodes'])
                        way_tags_writer.writerows(el['way_tags'])
                        
                        
        print None


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    process_map(OSM_PATH, validate=True)
