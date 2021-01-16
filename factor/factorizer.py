import jqdatasdk as jq


account = "18620156503"
password = "3DKkypzN6uPj"
jq.auth(account,password)
print ("login successed!")    
remain_query = jq.get_query_count()
print ("remain query times for jqdata: ",remain_query)   



def p_perday_var(start_date,end_date):
    tradeable_days = get_trade_days(start_date=start_date, end_date=end_date)
    for trade_day in tradeable_days:
        stock_code_list = jq.get_all_securities(date = trade_day)
        result = jq.get_price(list(stock_code_list), start_date=trade_day, end_date=trade_day, frequency='daily', fields=['close'], skip_paused=False, fq='pre', count=None, panel=True, fill_paused=True)
        
