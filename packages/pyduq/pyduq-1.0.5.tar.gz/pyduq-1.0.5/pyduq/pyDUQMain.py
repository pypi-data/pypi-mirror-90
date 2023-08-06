""" pyduqmain.py

Overview
--------
pyduq is a data quality validation tool that implements
the LANG data quality algorithms 
(see: Zhang, R., Indulska, M., & Sadiq, S. (2019). Discovering Data Quality Problems: The Case of Repurposed Data. 
Business and Information Systems Engineering, 61(5), 575–593. https://doi.org/10.1007/s12599-019-00608-0


USAGE
--------

$ python pyduqmain.py -h

usage: pyduqmain.py [-h] [-i INPUTFILE] [-o OUTPUTFOLDER] [-m METAFILE]
                    [-s SQL SQL] [-c CUSTOM] [-p] [-v] [--infer] [--verbose]

Perform a data quality validation.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUTFILE, --inputfile INPUTFILE
                        the path and name of the input data file
                        to use as the data source.
  -o OUTPUTFOLDER, --outputfolder OUTPUTFOLDER
                        the destination path for the output files to be
                        stored.
  -m METAFILE, --metafile METAFILE
                        the filename of the metadata-data file to use for
                        validation.
  -s SQL SQL, --sql SQL SQL
                        a database connection string and SQL query to use 
                        as the data source.
  -c CUSTOM, --custom CUSTOM
                        The class path and name of a custom validator.
  -p, --profile         profile the data.
  -v, --validate        validate the data.
  --infer               Generate metadata.
  --extend              Must be used with -m switch. Extends the provided
                        meatdata file with any additional attributes or
                        rules found in the data source. Overwrites the 
                        suppled metafile.
  --verbose             Generate verbose output.


OUTPUT:
--------
The outout from pylang depends on what you want to achieve.
the --profile switch will trigger a data profile the source data 
and output the results as an Excel spreadsheet.

The --validate switch will trigger a validation of the source
data and the output will be a Spreadsheet of data quality
validation errors.

The --infer swutch will force the metadata to be inferred from the
data. (Note - if -v is used and there is no metadata provided then
--infer will be set).

The --profile switch generates a profile data file.

The --extend will take an existing metadatafile, compare it with the source data, and
extend the metadata by adding any missing columns or extending attribute lengths. It
will also extend enum types where found. 


"""
#!/usr/bin/python

import sys
import os
import argparse
import pyodbc
import time
from pyduq.abstractduqvalidator import AbstractDUQValidator
from pyduq.SQLTools import SQLTools
from pyduq.duqvalidator import DUQValidator
from pyduq.patterns import Patterns
from pyduq.duqerror import ValidationError
from pyduq.filetools import FileTools
from pyduq.dataprofile import DataProfile


class pyDUQMain(object):

    def __init__(self, inputFile:str, outputFolder:str="", filePrefix:str="", metaFile:str="", customValidator:str="", sqlURI:str="", sqlQuery:str=""):
        self.metadata = {}
        self.dataset = {}
        self.inputFile = (inputFile if not inputFile is None else "sql-query")
        self.metaFile = metaFile
        self.outputFolder = (outputFolder if not outputFolder is None else ".")
        self.customValidator = customValidator
        self.sqlURI = sqlURI
        self.sqlQuery = sqlQuery
        
        if ((not filePrefix is None) and (len(filePrefix) > 0)):
            self.outputFilePrefix = filePrefix
        else:
            self.outputFilePrefix = self.inputFile.rsplit(".", 1)[0]
            if (self.outputFilePrefix.endswith("-") or self.outputFilePrefix.endswith("_")):
                self.outputFilePrefix = self.outputFilePrefix[:-1]
       
       
    def loadSQL(self):
        cnxn = pyodbc.connect(self.sqlURI)
        cursor = cnxn.cursor()
        cursor.execute(self.sqlQuery) 
        self.dataset = SQLTools(cursor).dataset
        print("SQL query returned " + str(len(self.dataset)) + " columns.")


    def loadMeta(self, extendFlag:False):
        self.metadata = FileTools.JSONtoMeta(self.metaFile)
        if(extendFlag):
            self.metadata = FileTools.extendMeta(self.metadata, FileTools.inferMeta(self.dataset))
            if (self.metaFile is None or len(self.metaFile)==0):
                self.metaFile = self.outputFilePrefix + "_meta.json"
            FileTools.MetatoJSONFile(self.metaFile, self.metadata)
            print("Using extended metadata.")


    def inferMeta(self):
        stime = time.time()
        self.metadata = FileTools.inferMeta(self.dataset)
        if (self.metaFile is None or len(self.metaFile)==0):
            self.metaFile = self.outputFilePrefix + "_meta.json"
            
        FileTools.MetatoJSONFile(self.metaFile, self.metadata)
        print("Metadata file generated in " + str(time.time() - stime) + " secs")


    def loadCSV(self):
        self.dataset = FileTools.csvFileToDict(self.inputFile)
        print("CSV file loaded " + str(len(self.dataset)) + " columns.")

    
    def loadXLS(self, sheet:None):
        self.dataset = FileTools.xlsFileToDict(self.inputFile, sheet)
        print("Excel spreadsheet loaded " + str(len(self.dataset)) + " columns.")


    def validate(self):
        try:
            stime = time.time()
     
            lang_validator = DUQValidator(self.dataset, self.metadata)
            lang_validator.validate(self.customValidator)
            
            lang_validator.saveCounters(self.outputFilePrefix + "_counters.xlsx")
            lang_validator.saveCountersSummary(self.outputFilePrefix + "_summary.xlsx")
            
            print("Validation completed in " + str(time.time() - stime) + " secs")

        except ValidationError as e:
            print (e)


    def profile(self):
        try:
            stime = time.time()
            
            data_profile = DataProfile().profile(self.metadata, self.dataset)
            FileTools.saveProfile(self.outputFilePrefix + "_profile.xlsx", data_profile)
            
            print("Profile completed in " + str(time.time() - stime) + " secs")

        except ValidationError as e:
            print (e)

    
        
def main(argv):

    # Create the parser
    my_parser = argparse.ArgumentParser(description='Perform a data quality validation.')

    # Add the arguments
    my_parser.add_argument('-i',
                           '--inputfile',
                           type=str,
                           help='the path and name of the input data file.')

    my_parser.add_argument('-o',
                           '--outputfolder',
                           type=str,
                           help='the destination path for the output files to be stored.')
    
    my_parser.add_argument('-m',
                           '--metafile',
                           type=str,
                           help='the filename of the metadata-data file to use for validation.')
                           
    my_parser.add_argument('-s',
                           '--sql',
                           nargs=2,
                           type=str,
                           help='the database connection string and SQL query')
                           
    my_parser.add_argument('-c',
                           '--custom',
                           type=str,
                           help='The class path and name of a custom validator.')

    my_parser.add_argument('-f',
                           '--fileprefix',
                           type=str,
                           help='The prefix to use for all output files.')

    my_parser.add_argument('-S',
                           '--sheet',
                           type=str,
                           help='The name of the sheet to load from an Excel spreadsheet file.')

    my_parser.add_argument('-p',
                           '--profile',
                           action="store_true",
                           help='profile the data.')

    my_parser.add_argument('-v',
                           '--validate',
                           action="store_true",
                           help='validate the data.')

    my_parser.add_argument('--infer',
                           action="store_true",
                           help='Generate metadata.')

    my_parser.add_argument('--extend',
                           action="store_true",
                           help='Extend source metadata.')

    my_parser.add_argument('--verbose',
                           action="store_true",
                           help='Generate verbose output.')



    # Execute parse_args()
    args = my_parser.parse_args()
    sqlURI = ""
    sqlQuery = ""

    if ((not args.inputfile is None) and (len(args.inputfile)>0)):
        if not os.path.isfile(args.inputfile):
            print("The input file '" + args.inputfile + "' does not exist")
            sys.exit(1)
    else:
        if (args.sql is not None):
            sqlURI = args.sql[0]
            sqlQuery = args.sql[1]
        else:
            print("You must provide either an input file OR SQL connection and query. Run pyduqmain.py -h for help.")
            sys.exit(1)            

    pyduq = pyDUQMain(args.inputfile, args.outputfolder, args.fileprefix, args.metafile, args.custom, sqlURI, sqlQuery)

    profileFlag = args.profile
    validateFlag = args.validate
    inferFlag = args.infer
    extendFlag = args.extend
    __verbose__ = args.verbose
    

    
    if (len(sqlURI) >0 ):
        pyduq.loadSQL()
    elif (len(pyduq.inputFile)>0):
        if(pyduq.inputFile.endswith(".csv")):
            pyduq.loadCSV()
        elif(pyduq.inputFile.endswith(".xlsx") or pyduq.inputFile.endswith(".xltx")):
            pyduq.loadXLS(args.sheet)
        else:
            print("Unsupported source data file type. Run pyduqmain.py -h for help.")
            sys.exit(1)            

    if (not pyduq.metaFile is None):
        if (not os.path.isfile(pyduq.metaFile)):
            print("The metadata-data file '" + pyduq.metaFile + "' does not exist")
            sys.exit(1)
        pyduq.loadMeta(extendFlag)
    else:
        if (not inferFlag):
            print("No metadata file was supplied - schema will be inferred from the dataset.")
        pyduq.inferMeta()

    if (validateFlag):
        pyduq.validate()

    if (profileFlag):
        pyduq.profile()
        
    sys.exit(0)


if  __name__ =='__main__':
    main(sys.argv[1:])
