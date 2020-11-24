import psycopg2

class BaseTable(object):
    def __init__(self,sql_con,sql_cur):
        self.con = sql_con
        self.cur = sql_cur

    def getTableInfo(self,):
        pass

    def createTable(self,):
        pass

    def deleleTable(self,):
        pass

    def insertInfo(self,):
        pass