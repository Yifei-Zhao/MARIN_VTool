#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 8/15/19 12:46 AM

@author: nirav
"""
import pandas as pd
import DBConnection

class GetGridsLandData:
    '''
    Description:
    ------------
    It gets land, grids data from DB and CSV file.

    Note: make sure DB config file is set
    '''

    def __init__(self, **kwargs):
        self.dbConfigFile = kwargs.get('fileName','../DB/Config/DBConfig.xml')
        self.dbConnection = DBConnection.DBConnection(self.dbConfigFile)
        self.landDataCSV = kwargs.get('landFileName','../Data/Other/cp_coast_la.csv')
        self.gridsDataCSV = kwargs.get('gridsFileName','../Data/Other/amtgrids.csv')

    # get land data and return dataframe
    def getLandData(self):
        landData = []
        countryList = ['ca'] # add other countries here
        connection = self.dbConnection.getConnection()
        cursor = connection.cursor()

        for country in countryList:
            cursor.execute("select ogc_fid, wkb_geometry from cp_coast_la where country = '{}';".format(country))
            for row in cursor:
                landData.append(row)

        self.dbConnection.closeConnection(cursor, connection)
        landData = pd.DataFrame(landData, columns=['id','geom'])
        return landData

    # get grids data and return dataframe
    def getGridsData(self, **kwargs):
        tableName = kwargs.get('tablename', 'amtgrids')
        gridsData = []
        connection = self.dbConnection.getConnection()
        cursor = connection.cursor()

        cursor.execute("select id, mstrid, grid0_1, geom from {};".format(tableName))
        for row in cursor:
            gridsData.append(row)

        self.dbConnection.closeConnection(cursor, connection)
        gridsData = pd.DataFrame(gridsData, columns=['id','mstrid','grid0_1','geom'])
        return gridsData

    # get land data i.e. cp_coast_la from csv file
    def getLandDataFrmCSV(self):
        columns = ['ogc_fid', 'coast', 'coast_id', 'country', 'region', 'water', 'shape_leng', 'shape_area', 'geom']
        removeColumns = ['ogc_fid', 'coast', 'country', 'region', 'water', 'shape_leng', 'shape_area']
        self.landDataCSV = pd.read_csv(self.landDataCSV, sep=',', encoding='utf-8', names=columns)
        self.landDataCSV = self.landDataCSV.loc[self.landDataCSV['country'] == 'ca'] #only canada's data

        # removing extra columns from dataframe
        for i in removeColumns:
            del self.landDataCSV[i]

        return self.landDataCSV

    # get grids data from csv file
    def getGridsDataFrmCSV(self):
        columns = ['id', 'mstrid', 'f_p', 'f1_p', 'f2_p', 'f3_p', 'f4_p', 'grid0_1', 'grid0_25', 'grid0_5', 'geom']
        self.gridsDataCSV = pd.read_csv(self.gridsDataCSV, sep=',', encoding='utf-8', names=columns, index_col=False)
        removeColumns = ['id','f_p', 'f1_p', 'f2_p', 'f3_p', 'f4_p', 'grid0_25', 'grid0_5']

        # removing extra columns from dataframe
        for i in removeColumns:
            del self.gridsDataCSV[i]

        self.gridsDataCSV = self.gridsDataCSV.reset_index(drop = True)
        return self.gridsDataCSV