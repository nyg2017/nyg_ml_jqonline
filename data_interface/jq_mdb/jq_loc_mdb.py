import jqdatasdk as jq
import pymongo  
from data_interface.jq_mdb.table.price_table import PriceTable
from data_interface.jq_mdb.table.index_table import IndexTable
from data_interface.jq_mdb.table.turnover_ratio_table import TurnOverRatioTable
from data_interface.jq_mdb.table.trade_days_table import TradeDayTable
from data_interface.jq_mdb.table.all_security_table import AllSecurityTable
from data_interface.jq_mdb.table.unfq_price_table import UnfqPriceTable

class JqLocMongoDB(object):
    def __init__(self,):
        self.client = pymongo.MongoClient(host='localhost', port=27017) 
        self.database = self.client["jq_loc"]
        self.initTables()
        self.initJq()


    
    def initTables(self,):
        self.price_table = PriceTable(self.database,"price_table")
        self.index_table = IndexTable(self.database,"index_table")
        self.turnover_ratio_table = TurnOverRatioTable(self.database,"turnover_ratio_table")
        self.trade_days_table = TradeDayTable(self.database,"trade_days_table")
        self.all_security_table = AllSecurityTable(self.database,"all_security_table")
        self.unfq_price_table = UnfqPriceTable(self.database,"unfq_price_table")

        self.tables = [self.price_table,self.index_table,self.turnover_ratio_table,self.trade_days_table,self.all_security_table,self.unfq_price_table]


    def updateTables(self,start_date,end_date):

        for table in self.tables:
            table.insertInfo(start_date,end_date)
        # self.price_table.insertInfo(start_date,end_date)
        # self.index_table.insertInfo(start_date,end_date)
        # self.turnover_ratio_table.insertInfo(start_date,end_date)
        # self.trade_days_table.insertInfo(start_date,end_date)
        # self.all_security_table.insertInfo(start_date,end_date)
        # self.unfq_price_table.insertInfo(start_date,end_date)

    def reset_index(self,):
        for table in self.tables:
            table.dropIndex()
            table.createIndex()
        # self.price_table.createIndex()
        # self.index_table.createIndex()
        # self.turnover_ratio_table.createIndex()
        # self.trade_days_table.createIndex()
        # self.all_security_table.createIndex()
        # self.unfq_price_table.createIndex()


    def deleteDB(self,):
        self.database.command("dropDatabase")
        print ("empty_tables:",self.database.list_collection_names(session=None))
        print (self.database)

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
    start_date = "2020-01-01"
    end_date = "2020-11-30"
    #a.deleteDB()
    #a.updateTables(start_date,end_date)
    a.reset_index()
    #a.unfq_price_table.insertInfo(start_date,end_date)
    #@stock_list = ['300750.XSHE','300760.XSHE','300761.XSHE',"asd","adgagasdg"]
    #a.price_table.getPriceInfo(stock_list = stock_list,date = start_date,fields = "close")
    #r = a.price_table.fetch(start_date,stock_list,"close")

    #print (r)
    #a.price_table.createIndex()

