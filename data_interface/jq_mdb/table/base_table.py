import pymongo  

class BaseTable(object):
    def __init__(self,database,table_name):
        self.database = database
        self.table = self.database[table_name]
        self.table_name = table_name

    def getTableInfo(self,):
        print (self.table)

    def createTable(self,):
        pass

    def deleteTable(self):
        print (type(self.table))
        self.table.command("dropDatabase")
        print ("price table deleted")

    def dropIndex(self):
        self.table.drop_index()
    
    def insertInfo(self,):
        pass