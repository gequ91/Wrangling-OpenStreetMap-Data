#!/usr/bin/env python
# -*- coding: utf-8 -*-

def parseNds(element, way_nodes):
    ndDict = [{"id": element.attrib["id"], "node_id": nd.attrib["ref"], "position": i} for i, nd in enumerate(element.iter("nd"))]
    return ndDict