import jqdatasdk as jq
import pymongo  
from data_interface.jq_mdb.table.price_table import PriceTable

class QueryMongoDB(object):
    def __init__(self,):
        self.client = pymongo.MongoClient(host='localhost', port=27017) 
        self.initTables()
        self.initJq()

    def initTables(self,):
        self.price_table = PriceTable(self.client,"price_table")

    


    def initJq(self,):
        print ("login JQDATA servering")
        account = "15210089516"#"15210089516"
        password = "Ningyaguang1"
        account = "13132110856" # "18620156503"
        password = "Ningyaguang1"     #"3DKkypzN6uPj"

        #account = "18620156503"
        #password = "3DKkypzN6uPj"
        jq.auth(account,password)
        print ("login successed!")    
        remain_query = jq.get_query_count()
        print ("remain query times for jqdata: ",remain_query)



if __name__ == "__main__":
    a = QueryMongoDB()
    start_date = "2019-09-02"
    end_date = "2019-09-10"
    #a.price_table.deleteTable()
    #a.price_table.insertInfo(start_date,end_date)
    stock_list = ['300750.XSHE','300760.XSHE','300761.XSHE',"asd"]
    a.price_table.getPriceInfo(stock_list = stock_list,date = start_date,fields = "close")