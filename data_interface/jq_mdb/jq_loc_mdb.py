import jqdatasdk as jq
import pymongo  
from data_interface.jq_mdb.table.price_table import PriceTable
from data_interface.jq_mdb.table.index_table import IndexTable



class JqLocMongoDB(object):
    def __init__(self,):
        self.client = pymongo.MongoClient(host='localhost', port=27017) 
        self.database = self.client["jq_loc"]
        self.initTables()
        self.initJq()

    def initTables(self,):
        self.price_table = PriceTable(self.database,"price_table")
        self.index_table = IndexTable(self.database,"index_table")



    def initJq(self,):
        print ("login JQDATA servering")
        account = "15210089516"#"15210089516"
        password = "Ningyaguang1"
        account = "13132110856" # "18620156503"
        password = "Ningyaguang1"     #"3DKkypzN6uPj"

        account = "18620156503"
        password = "3DKkypzN6uPj"
        jq.auth(account,password)
        print ("login successed!")    
        remain_query = jq.get_query_count()
        print ("remain query times for jqdata: ",remain_query)



if __name__ == "__main__":
    a = JqLocMongoDB()
    start_date = "2019-01-01"
    end_date = "2019-12-31"
    #a.price_table.deleteTable()
    a.index_table.insertInfo(start_date,end_date)
    a.price_table.insertInfo(start_date,end_date)
    #@stock_list = ['300750.XSHE','300760.XSHE','300761.XSHE',"asd","adgagasdg"]
    #a.price_table.getPriceInfo(stock_list = stock_list,date = start_date,fields = "close")
    #r = a.price_table.fetch(start_date,stock_list,"close")

    #print (r)
    #a.price_table.createIndex()

