import jqdatasdk as jq
import numpy as np
import pandas as pd
from date_interface.jq_data_online import login
import datetime,os
from util.jqdata_processor import dateArr2List


def updatePriceData(trade_day_list):
    fields = ['open', 'close', 'low', 'high', 'volume', 'money', 'factor', 'high_limit','low_limit', 'avg', 'pre_close', 'paused', 'open_interest']
    root_dir = "./DATA/jq_data/price"
    file_list = os.listdir(root_dir)
    for date_time in trade_day_list:
        if date_time not in file_list:
            print (date_time)
            stock_code_list = jq.get_all_securities(types=['stock'], date=date_time).index

            price = jq.get_price(list(stock_code_list), start_date=date_time, end_date=date_time, frequency='daily', fields = fields , skip_paused=False, fq='pre', count=None, panel=True, fill_paused=True)
            price.to_csv(os.path.join(root_dir,date_time),index=False)

    print ("update price data finished! from %s to %s",trade_day_list[0],trade_day_list[-1])


def updateLocalData(start_date = "2012-01-01",end_data = datetime.datetime.today()):
    login()
    trade_day_list = dateArr2List(jq.get_trade_days(start_date=start_date, end_date=end_data))
    updatePriceData(trade_day_list)





if __name__ == "__main__":

    start_date = "2012-01-01"
    end_data = "2012-01-06"
    #updateLocalData(start_date)

    # login()
    # date_time = "2019-09-04"
    # _date_time = "2019-09-06"
    # stock_code_list = jq.get_all_securities(types=['stock'], date=None).index
    # print (stock_code_list)
    # fields = ['open', 'close', 'low', 'high', 'volume', 'money', 'factor', 'high_limit','low_limit', 'avg', 'pre_close', 'paused', 'open_interest']

    # price = jq.get_price(list(stock_code_list), start_date=date_time, end_date=_date_time, frequency='daily', fields = fields,skip_paused=False, fq='pre', count=None, panel=True, fill_paused=True) 
    # print (price)
    # price.to_csv(str(date_time),index=False) 

    price = pd.read_csv(os.path.join("./DATA/jq_data/price",end_data))
    a = price['close'].values
    print (type(price['close'].values))
    v = np.isnan(a)
    print (a[~v])
