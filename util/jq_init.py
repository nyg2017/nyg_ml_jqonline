
import jqdatasdk as jq


def login():
    print ("login JQDATA servering")
    account = "15210089516"
    password = "Ningyaguang1"
    jq.auth(account,password)
    print ("login successed!")    
    remain_query = jq.get_query_count()
    print ("remain query times for jqdata: ",remain_query)