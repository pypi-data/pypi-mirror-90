import re
import uuid
import numpy as np
import pandas as pd
from dolphindb.table import Table
from dolphindb.database import Database
from dolphindb.settings import *
from threading import Lock
from datetime import datetime

import os
import sys
import asyncio
from concurrent.futures import ThreadPoolExecutor

sys.path.append(os.path.dirname(__file__))

import dolphindbcpp  as ddbcpp

def _generate_tablename():
    return "TMP_TBL_" + uuid.uuid4().hex[:8]


def _generate_dbname():
    return "TMP_DB_" + uuid.uuid4().hex[:8]+"DB"

class DBConnectionPool(object):
    def __init__(self, host, port, threadNum=10, userid="", password="", clearSessionMemory=True, reConnectFlag=True):
        self.pool = ddbcpp.dbConnectionPoolImpl(host, port, threadNum, userid, password, clearSessionMemory, reConnectFlag)
        self.host = host
        self.port = port
        self.userid = userid
        self.password = password
        self.taskId = 0
        self.mutex = Lock()

    async def run(self, script):
        self.mutex.acquire()
        self.taskId = self.taskId + 1
        id = self.taskId
        self.mutex.release()
        self.pool.run(script, id)
        while True:
            isFinished = self.pool.isFinished(id)
            if(isFinished == 0):
                await asyncio.sleep(0.01)
            else:
                return self.pool.getData(id)
    
    def shutDown(self):
        self.host = None
        self.port = None
        self.pool.shutDown()

class session(object):
    """
    dolphindb api class
    connect: initiate socket connection
    run: execute dolphindb script and return corresponding python objects
    1: Scalar variable returns a python scalar
    2: Vector object returns numpy array
    3: Table object returns  a pandas data frame
    4: Matrix object returns a numpy array
    """
    def __init__(self, host=None, port=None, userid="", password="",enableSSL=False, enableASYN=False):
        self.cpp = ddbcpp.sessionimpl(enableSSL,enableASYN)
        self.host = host
        self.port = port
        self.userid = userid
        self.password=password
        self.mutex = Lock()
        self.enableEncryption = True
        if self.host is not None and self.port is not None:
            self.connect(host, port, userid, password)

    def connect(self, host, port, userid="", password="", startup="", highAvailability=False, highAvailabilitySites=[]):
        return self.cpp.connect(host, port, userid, password, startup, highAvailability, highAvailabilitySites)

    def login(self,userid, password, enableEncryption=True):
        self.mutex.acquire()
        try:
            self.userid = userid
            self.password = password
            self.enableEncryption = enableEncryption
            self.cpp.login(userid, password, enableEncryption)
        finally:
            self.mutex.release()

    def close(self):
        self.host = None
        self.port = None
        self.cpp.close()

    def upload(self, nameObjectDict):
        return self.cpp.upload(nameObjectDict)

    def run(self, script, *args):
        return self.cpp.run(script, *args)

    def nullValueToZero(self):
        self.cpp.nullValueToZero()
    
    def nullValueToNan(self):
        self.cpp.nullValueToNan()

    def enableStreaming(self, port):
        self.cpp.enableStreaming(port)

    def subscribe(self, host, port, handler, tableName, actionName="", offset=-1, resub=False, filter=None, msgAsTable=False):
        if filter is None:
            filter = np.array([],dtype='int64')
        self.cpp.subscribe(host, port, handler, tableName, actionName, offset, resub, filter, msgAsTable)

    def unsubscribe(self, host, port, tableName, actionName=""):
        self.cpp.unsubscribe(host, port, tableName, actionName)

    def hashBucket(self, obj, nBucket):
        if not isinstance(nBucket, int) or nBucket <= 0:
            raise ValueError("nBucket must be a positive integer")
        return self.cpp.hashBucket(obj, nBucket)

    def getInitScript(self):
        return self.cpp.getInitScript()

    def setInitScript(self, script):
        self.cpp.setInitScript(script)

    def getSubscriptionTopics(self):
        return self.cpp.getSubscriptionTopics()

    def saveTable(self, tbl, dbPath):
        tblName = tbl.tableName()
        dbName =  _generate_dbname()
        s1 = dbName+"=database('"+dbPath+"')"
        self.run(s1)
        s2 = "saveTable(%s, %s)" % (dbName, tblName)
        self.run(s2)
        return True

    def loadText(self,  remoteFilePath=None, delimiter=","):
        tableName = _generate_tablename()
        runstr = tableName + '=loadText("' + remoteFilePath + '","' + delimiter + '")'
        self.run(runstr)
        return Table(data=tableName, s=self)

    def ploadText(self, remoteFilePath=None, delimiter=","):
        tableName = _generate_tablename()
        runstr = tableName + '= ploadText("' + remoteFilePath + '","' + delimiter + '")'
        self.run(runstr)
        return Table(data=tableName, s=self)

    def loadTable(self,tableName,  dbPath=None, partitions=None, memoryMode=False):
        """
        :param dbPath: DolphinDB table db path
        :param tableName: DolphinDB table name
        :param partitions: partitions to be loaded when specified
        :param memoryMode: loadTable all in ram or not
        :return:a Table object
        """
        def isDate(s):
            try:
                datetime.strptime(s, '%Y.%m.%d')
                return True
            except ValueError:
                return False

        def isMonth(s):
            try:
                datetime.strptime(s, '%Y.%mM')
                return True
            except ValueError:
                return False

        def isDatehour(s):
            try:
                datetime.strptime(s, '%Y.%m.%dT%H')
                return True
            except ValueError:
                return False

        def isTime(s):
            return isDate(s) or isMonth(s) or isDatehour(s)

        def myStr(x):
            if type(x) is str and not isTime(x):
                return "'" + x + "'"
            else:
                return str(x)

        if partitions is None:
            partitions = []
        if dbPath:
            runstr = '{tableName} = loadTable("{dbPath}", "{data}",{partitions},{inMem})'
            fmtDict = dict()
            tbName = _generate_tablename()
            fmtDict['tableName'] = tbName
            fmtDict['dbPath'] = dbPath
            fmtDict['data'] = tableName
            if type(partitions) is list:
                fmtDict['partitions'] = ('[' + ','.join(myStr(x) for x in partitions) + ']') if len(partitions) else ""
            else:
                fmtDict['partitions'] = myStr(partitions)

            fmtDict['inMem'] = str(memoryMode).lower()
            runstr = re.sub(' +', ' ', runstr.format(**fmtDict).strip())
            self.run(runstr)
            return Table(data=tbName, s=self)
        else:
            return Table(data=tableName, s=self, needGC=False)

    def loadTableBySQL(self, tableName, dbPath, sql):
        """
        :param tableName: DolphinDB table name
        :param dbPath: DolphinDB table db path
        :param sql: sql query to load the data
        :return:a Table object
        """
        # loadTableBySQL
        runstr = 'db=database("' + dbPath + '")'
        # print(runstr)
        self.run(runstr)
        runstr = tableName + '= db.loadTable("%s")' % tableName
        # print(runstr)
        self.run(runstr)
        runstr = tableName + "=loadTableBySQL(<%s>)" % sql
        # runstr =  sql
        # print(runstr)
        self.run(runstr)
        return Table(data=tableName, s=self)

    def convertDatetime64(self, datetime64List):
        l = len(str(datetime64List[0]))
        # date and month
        if l == 10 or l == 7:
            listStr = '['
            for dt64 in datetime64List:
                s = str(dt64).replace('-', '.')
                if len(str(dt64)) == 7:
                    s += 'M'
                listStr += s + ','
            listStr = listStr.rstrip(',')
            listStr += ']'
        else:
            listStr = 'datehour(['
            for dt64 in datetime64List:
                s = str(dt64).replace('-', '.').replace('T', ' ')
                ldt = len(str(dt64))
                if ldt == 13:
                    s += ':00:00'
                elif ldt == 16:
                    s += ':00'
                listStr += s + ','
            listStr = listStr.rstrip(',')
            listStr += '])'
        return listStr


    def convertDatabase(self, databaseList):
        listStr = '['
        for db in databaseList:
            listStr += db._getDbName()
            listStr += ','
        listStr = listStr.rstrip(',')
        listStr += ']'
        return listStr

    def database(self,dbName=None, partitionType=None, partitions=None, dbPath=None):
        """

        :param dbName: database variable Name on DolphinDB Server
        :param partitionType: database Partition Type
        :param partitions: partitions as a python list
        :param dbPath: database path
        :return:
        """
        if partitions is not None:
            partition_type = type(partitions[0])
        else:
            partition_type = None

        if partition_type == np.datetime64:
            partition_str = self.convertDatetime64(partitions)

        elif partition_type == Database:
            partition_str = self.convertDatabase(partitions)

        elif type(partitions) == np.ndarray and (partition_type == np.ndarray or partition_type == list):
            dataType = type(partitions[0][0])
            partition_str = '['
            for partition in partitions:
                if dataType == date or dataType == month:
                    partition_str += self.convertDateAndMonth(partition) + ','
                elif dataType == datetime:
                    partition_str += self.convertDatetime(partition) + ','
                elif dataType == Database:
                    partition_str += self.convertDatabase(partition) + ','
                else:
                    partition_str += str(partition) + ','
                    partition_str = partition_str.replace('list', ' ')
                    partition_str = partition_str.replace('(', '')
                    partition_str = partition_str.replace(')', '')
            partition_str = partition_str.rstrip(',')
            partition_str += ']'

        else:
            if partition_type is not None:
                partition_str = str(partitions)
            else:
                partition_str = ""

        if dbName is None:
            dbName = _generate_dbname()

        if partitionType:
            if dbPath:
                dbstr =  dbName + '=database("'+dbPath+'",' + str(partitionType) + "," + partition_str + ")"
            else:
                dbstr =  dbName +'=database("",' + str(partitionType) + "," + partition_str + ")"
        else:
            if dbPath:
                dbstr =  dbName +'=database("' + dbPath + '")'
            else:
                dbstr =  dbName +'=database("")'

        self.run(dbstr)
        return Database(dbName=dbName, s=self)

    def existsDatabase(self, dbUrl):
        return self.run("existsDatabase('%s')" % dbUrl)

    def existsTable(self, dbUrl, tableName):
        return self.run("existsTable('%s','%s')" % (dbUrl,tableName))

    def dropDatabase(self, dbPath):
        self.run("dropDatabase('" + dbPath + "')")

    def dropPartition(self, dbPath, partitionPaths, tableName=None):
        """

        :param dbPath: a DolphinDB database path
        :param partitionPaths:  a string or a list of strings. It indicates the directory of a single partition or a list of directories for multiple partitions under the database folder. It must start with "/"
        :param tableName:a string indicating a table name.
        :return:
        """
        db = _generate_dbname()
        self.run(db + '=database("' + dbPath + '")')
        if isinstance(partitionPaths, list):
            pths = ','.join(partitionPaths)
        else:
            pths = partitionPaths

        if tableName:
            self.run("dropPartition(%s,[%s],\"%s\")" % (db, pths, tableName))
        else:
            self.run("dropPartition(%s,[%s])" % (db, pths))

    def dropTable(self, dbPath, tableName):
        db = _generate_dbname()
        self.run(db + '=database("' + dbPath + '")')
        self.run("dropTable(%s,'%s')" % (db,tableName))

    def loadTextEx(self, dbPath="", tableName="",  partitionColumns=None, remoteFilePath="", delimiter=","):
        """
        :param tableName: loadTextEx table name
        :param dbPath: database path, when dbPath is empty, it is in-memory database
        :param partitionColumns: partition columns as a python list
        :param remoteFilePath:the file to load into database
        :param delimiter:
        :return: a Table object
        """
        if partitionColumns is None:
            partitionColumns = []
        isDBPath = True
        if "/" in dbPath or "\\" in dbPath or "dfs://" in dbPath:
            dbstr ='db=database("' + dbPath + '")'
        # print(dbstr)
            self.run(dbstr)
            tbl_str = '{tableNameNEW} = loadTextEx(db, "{tableName}", {partitionColumns}, "{remoteFilePath}", {delimiter})'
        else:
            isDBPath = False
            tbl_str = '{tableNameNEW} = loadTextEx('+dbPath+', "{tableName}", {partitionColumns}, "{remoteFilePath}", {delimiter})'
        fmtDict = dict()
        fmtDict['tableNameNEW'] = _generate_tablename()
        fmtDict['tableName'] = tableName
        fmtDict['partitionColumns'] = str(partitionColumns)
        fmtDict['remoteFilePath'] = remoteFilePath
        fmtDict['delimiter'] = delimiter
        # tbl_str = tableName+'=loadTextEx(db,"' + tableName + '",'+ str(partitionColumns) +',"'+ remoteFilePath+"\",'"+delimiter+"')"
        tbl_str = re.sub(' +', ' ', tbl_str.format(**fmtDict).strip())
        self.run(tbl_str)
        if isDBPath:
            return Table(data=fmtDict['tableName'] , dbPath=dbPath, s=self)
        else:
            return Table(data=fmtDict['tableNameNEW'], s=self)

    def undef(self, varName, varType):
        undef_str = 'undef("{varName}", {varType})'
        fmtDict = dict()
        fmtDict['varName'] = varName
        fmtDict['varType'] = varType
        self.run(undef_str.format(**fmtDict).strip())

    def undefAll(self):
        self.run("undef all")

    def clearAllCache(self, dfs=False):
        if dfs:
            self.run("pnodeRun(clearAllCache)")
        else:
            self.run("clearAllCache()")

    def table(self, data, dbPath=None):
        return Table(data=data, dbPath=dbPath, s=self)

    def table(self, dbPath=None, data=None,  tableAliasName=None, inMem=False, partitions=None):
        """
        :param data: pandas dataframe, python dictionary, or DolphinDB table name
        :param dbPath: DolphinDB database path
        :param tableAliasName: DolphinDB table alias name
        :param inMem: load the table in memory or not
        :param partitions: the partition column to be loaded into memory. by default, load all
        :return: a Table object
        """
        if partitions is None:
            partitions = []
        return Table(dbPath=dbPath, data=data,  tableAliasName=tableAliasName, inMem=inMem, partitions=partitions, s=self)

