from sqlalchemy import create_engine
import jqdatasdk as jq
import pymysql
from data_interface.jq_mysql.table.price_table import PriceTable

'''
class QueryMysql(object):
    def __init__(self,database="postgres",\
                user="postgres",
                password="123456",
                host="127.0.0.1",
                port="5432"):
        self.con = psycopg2.connect(database=database, user=user, password=password, host=host, port=port) 
        self.cur = con.cursor()
        self.initTables()

    def initTables(self,):
        self.price_table = PriceTable(self.con,self.cur)
'''
class QueryMysql(object):
    def __init__(self,database="jq_loc",\
                user="root",
                password="12345678",
                host="127.0.0.1",
                port="3306"):
        self.con = pymysql.connect(host=host,
                             user=user,
                             password=password,
                             db=database,
                             charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()
        self.initTables()
        self.initJq()

    def initTables(self,):
        self.price_table = PriceTable(self.con,self.cur)
    

    def initJq(self,):
        print ("login JQDATA servering")
        account = "15210089516"#"15210089516"
        password = "Ningyaguang1"
        #account = "13132110856" # "18620156503"
        #password = "Ningyaguang1"     #"3DKkypzN6uPj"

        #account = "18620156503"
        #password = "3DKkypzN6uPj"
        jq.auth(account,password)
        print ("login successed!")    
        remain_query = jq.get_query_count()
        print ("remain query times for jqdata: ",remain_query)


if __name__ == "__main__":
    my_sql_q = QueryMysql()
    start_date = "2020-09-13"
    end_date = "2020-09-14"
    my_sql_q.price_table.deleleTable()
    my_sql_q.price_table.createTable()
    my_sql_q.price_table.insertInfo(start_date,end_date)
    