import pymongo  

class BaseTable(object):
    def __init__(self,client,table_name):
        self.client = client
        self.table = self.client[table_name]
        self.table_name = table_name

    def getTableInfo(self,):
        print (self.table)

    def createTable(self,):
        pass

    def deleteTable(self):
        print (type(self.table))
        self.table.command("dropDatabase")
        print ("price table deleted")

    def insertInfo(self,):
        pass