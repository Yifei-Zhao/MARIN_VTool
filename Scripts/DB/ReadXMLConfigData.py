#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 7/12/19 6:30 PM

@author: nirav
"""
import xml.etree.ElementTree as ET

class ReadXMLConfigData:
    '''
    Description:
    ------------
    Read XML file and return all values in list

    Parameters:
    -----------
    **kwargs :
             inputFile : input xml file
    '''

    def __init__(self, inputFile):
        self.inputFile = inputFile

    def readXMLData(self):
        try:
            data = []
            root = ET.parse(self.inputFile).getroot()
            for child in root:
                data.append([child.tag, child.get('value')])
            return data
        except Exception as e:
            print(e)