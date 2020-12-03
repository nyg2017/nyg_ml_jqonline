from data_interface.jq_data_online import login
import time


def QA_util_date_stamp(date):
    """
    explanation:
        转换日期时间字符串为浮点数的时间戳
    
    params:
        * date->
            含义: 日期时间
            类型: str
            参数支持: []
    
    return:
        time
    """
    datestr = str(date)[0:10]
    date = time.mktime(time.strptime(datestr, '%Y-%m-%d'))
    return date


def QA_util_time_stamp(time_):
    """
    explanation:
       转换日期时间的字符串为浮点数的时间戳
    
    params:
        * time_->
            含义: 日期时间
            类型: str
            参数支持: ['2018-01-01 00:00:00']
    return:
        time
    """
    if len(str(time_)) == 10:
        # yyyy-mm-dd格式
        return time.mktime(time.strptime(time_, '%Y-%m-%d'))
    elif len(str(time_)) == 16:
        # yyyy-mm-dd hh:mm格式
        return time.mktime(time.strptime(time_, '%Y-%m-%d %H:%M'))
    else:
        timestr = str(time_)[0:19]
        return time.mktime(time.strptime(timestr, '%Y-%m-%d %H:%M:%S'))


def __transform_jq_to_qa(df, code, type_):
    if df is None or len(df) == 0:
        raise ValueError("没有聚宽数据")

    df["datetime"] = df.time
    #df["code"] = code
    df["date"] = df.datetime.map(str).str.slice(0, 10)
    df = df.set_index("datetime", drop=False)
    df["date_stamp"] = df["date"].apply(lambda x: QA_util_date_stamp(x))
    df["time_stamp"] = (
        df["datetime"].map(str).apply(lambda x: QA_util_time_stamp(x)))
    df["type"] = type_

    return df[[
        "open",
        "close",
        "high",
        "low",
        "volume",
        "money",
        "datetime",
        "code",
        "date",
        "date_stamp",
        "time_stamp",
        "type",
    ]]

def transform_2_jq_loc(df):
    #def __transform_jq_to_qa(df, code, type_):
        if df is None or len(df) == 0:
            raise ValueError("没有聚宽数据")

        df["datetime"] = df.time
        #df["code"] = code
        df = df.set_index("datetime", drop=False)
        df["date_stamp"] = df["datetime"].apply(lambda x: QA_util_date_stamp(x))

        return df[[
            "code",
            "open",
            "close",
            "high",
            "low",
            "volume",
            "money",
            "datetime",
            "date_stamp",
        ]]



if __name__ == "__main__":
    import jqdatasdk as jq
    login()
    start_date = "2019-09-02"
    end_date = "2019-09-10"
    #a.price_table.deleteTable()
    #a.price_table.insertInfo(start_date,end_date)
    stock_list = ['300750.XSHE','300760.XSHE','300761.XSHE']
    #result = jq.get_bars(stock_list, count = 5, unit='1m',
    #     fields=['date', 'open', 'close', 'high', 'low', 'volume', 'money','factor'],
    #     include_now=False, end_dt=None, fq_ref_date=None,df=True)
         
    result = jq.get_price(list(stock_list), start_date=start_date, end_date=start_date, frequency='daily', skip_paused=False, fq='pre', count=None, panel=True, fill_paused=True)
    a = transform_2_jq_loc(result)
    
    import numpy as np
    np.set_printoptions(suppress=True)
    print (a)