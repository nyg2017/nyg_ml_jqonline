import jqdatasdk as jq


def login():
    print ("login JQDATA servering")
    account = "15210089516"
    password = "Ningyaguang1"
    jq.auth(account,password)
    print ("login successed!")    
    remain_query = jq.get_query_count()
    print ("remain query times for jqdata: ",remain_query)

def getClosePrices(date_time,stock_code_list):
    result = jq.get_price(stock_code_list, start_date=date_time, end_date=date_time, frequency='daily', fields=['close'], skip_paused=False, fq='pre', count=None, panel=True, fill_paused=True)
    code = list(result['code'])
    cps = list(result['close'])
    code_cps_dict = dict(zip(code,cps))
    return [code_cps_dict[k] for k in stock_code_list]


def limitedTest(date_time,stock_code_list):
    result = jq.get_price(stock_code_list, start_date=date_time, end_date=date_time, frequency='daily', fields=['high','low'], skip_paused=False, fq='pre', count=None, panel=True, fill_paused=True)
    var = list(result['high'] - result['low'])
    code = list(result['code'])
    code_limit_dict = dict(zip(code,var))
    return ([code_limit_dict[k] == 0 for k in stock_code_list])

def getIndexValue(date_time,index):
    result = jq.get_price(index, start_date=date_time, end_date=date_time, frequency='daily', fields=['close'], skip_paused=False, fq='pre', count=None, panel=True, fill_paused=True)
    return result['close'].values


if __name__ == "__main__":
    login()
    code = ["300313.XSHE"]
    date_time = "2020-09-11"
    limitedTest(date_time,code)