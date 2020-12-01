from data_interface.jq_data_online import login


def __transform_jq_to_qa(df, code, type_):
    """
    处理 jqdata 分钟数据为 qa 格式，并存入数据库
    1. jdatasdk 数据格式:
                        open  close   high    low     volume       money
    2018-12-03 09:31:00  10.59  10.61  10.61  10.59  8339100.0  88377836.0
    2. 与 QUANTAXIS.QAFetch.QATdx.QA_fetch_get_stock_min 获取数据进行匹配，具体处理详见相应源码
                        open  close   high    low           vol        amount    ...
    datetime
    2018-12-03 09:31:00  10.99  10.90  10.99  10.90  2.211700e+06  2.425626e+07 ...
    """

    if df is None or len(df) == 0:
        raise ValueError("没有聚宽数据")

    df = df.reset_index().rename(columns={
        "index": "datetime",
        "volume": "vol",
        "money": "amount"
    })

    #df["code"] = code
    df["date"] = df.datetime.map(str).str.slice(0, 10)
    df = df.set_index("datetime", drop=False)
    df["date_stamp"] = df["date"]#.apply(lambda x: QA_util_date_stamp(x))
    df["time_stamp"] = (
        df["datetime"])#.map(str).apply(lambda x: (x)))
    df["type"] = type_

    return df[[
        "open",
        "close", 
        "high",
        "low",
        "vol",
        "amount",
        "datetime",
        "code",
        "date",
        "date_stamp",
        "time_stamp",
        "type",
    ]]



if __name__ == "__main__":
    import jqdatasdk as jq
    login()
    start_date = "2019-09-02"
    end_date = "2019-09-10"
    #a.price_table.deleteTable()
    #a.price_table.insertInfo(start_date,end_date)
    stock_list = ['300750.XSHE','300760.XSHE','300761.XSHE']
    result = jq.get_price(list(stock_list), start_date=start_date, end_date=start_date, frequency='daily', skip_paused=False, fq='pre', count=None, panel=True, fill_paused=True)
    a = __transform_jq_to_qa(result,stock_list,None)
    print (a)