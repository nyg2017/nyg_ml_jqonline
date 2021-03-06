import jqdatasdk as jq
import numpy as np

def login():
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

def getClosePrices(date_time,stock_code_list):
    result = jq.get_price(list(stock_code_list), start_date=date_time, end_date=date_time, frequency='daily', fields=['close'], skip_paused=False, fq='pre', count=None, panel=True, fill_paused=True)
    code = list(result['code'])
    cps = list(result['close'])
    code_cps_dict = dict(zip(code,cps))
    return np.array([code_cps_dict[k] for k in stock_code_list])


def getVolumn(date_time,stock_code_list):
    result = jq.get_price(list(stock_code_list), start_date=date_time, end_date=date_time, frequency='daily', fields=['volume'], skip_paused=False, fq='pre', count=None, panel=True, fill_paused=True)
    code = list(result['code'])
    cps = list(result['volume'])
    code_cps_dict = dict(zip(code,cps))
    return np.array([code_cps_dict[k] for k in stock_code_list])
    

def getTurnoverRatio(date_time,stock_code_list):
    query = jq.query(
                 jq.valuation.turnover_ratio
                 ).filter(jq.valuation.code.in_(stock_code_list))
    
    
    result = jq.get_fundamentals_continuously(query, end_date=date_time, count=1)
    print (result)
    #result = jq.get_fundamentals_continuously(query, start_date=date_time,end_date=date_time)
    code = list(result['code'])
    cps = list(result['turnover_ratio'])
    code_cps_dict = dict(zip(code,cps))
    return np.array([code_cps_dict[k] for k in stock_code_list])

def getIndexValue(date_time,index):
    result = jq.get_price(index, start_date=date_time, end_date=date_time, frequency='daily', fields=['close'], skip_paused=False, fq='pre', count=None, panel=True, fill_paused=True)
    return result['close'].values


def getSuspensionInfor(date_time,stock_list):
    suspened_info_df = jq.get_price(list(stock_list), 
                       start_date=date_time, 
                       end_date=date_time, 
                       frequency='daily', 
                       fields='paused')#['paused'].T
    code = suspened_info_df['code']
    var = suspened_info_df['paused']
    sus_dict = dict(zip(code,var))
    return np.array([sus_dict[k] == 0 for k in stock_list])


def getLimitInfor(date_time,stock_list):
    result = jq.get_price(list(stock_list), start_date=date_time, end_date=date_time, frequency='daily', fields=['high','low'], skip_paused=False, fq='pre', count=None, panel=True, fill_paused=True)
    var = list(result['high'] - result['low'])
    code = list(result['code'])
    code_limit_dict = dict(zip(code,var))
    return np.array([code_limit_dict[k] != 0 for k in stock_list])

def validIndex(date_time,stock_list):
    a = getSuspensionInfor(date_time,stock_list)
    b = getLimitInfor(date_time,stock_list)
    v = np.logical_and(a,b)
    return v

def isPublic(date_time,stock_list):
    v = np.zeros(len(stock_list),dtype = np.int)
    #result = jq.get_price(list(stock_list), start_date=date_time, end_date=date_time, frequency='daily', fields=['paused'], skip_paused=False, fq='pre', count=None, panel=True, fill_paused=True)
    result = jq.get_all_securities(types=[], date=date_time)
    #print (result)
    code_list = list(result.index)
    for i,stock in enumerate(stock_list):
        if stock in code_list:
            v[i] = 1
    
    return v.astype(np.bool)


if __name__ == "__main__":
    login()
    code = ['300014.XSHE']
    date_time = "2020-03-02"
    date_time_2 = "2020-03-03"
    #code = ['002100.XSHE']
    #a = jq.get_price(list(code), start_date=date_time, end_date=date_time, frequency='daily', fields=['high','low'], skip_paused=False, fq='pre', count=None, panel=True, fill_paused=True)
    p = getClosePrices(date_time = date_time,stock_code_list = code)
    print (p)
    p1 = getClosePrices(date_time = date_time_2,stock_code_list = code)
    print (p)
    print ((p1 - p) / p)

