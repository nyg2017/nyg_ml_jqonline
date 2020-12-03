import psycopg2
from data_interface.jq_mysql.table.base_table import BaseTable
import jqdatasdk as jq
import pandas as pd

fields = ['open', 'close', 'low', 'high', 'volume', 'money', 'factor', 'high_limit','low_limit', 'avg', 'pre_close', 'paused', 'open_interest']


class PriceTable(BaseTable):
    # def __init__(self,sql_con,sql_cur):
    #     self.con = sql_con
    #     self.sql_cur = sql_cur

    def getTableInfo(self,):
        info = """ TABLE    沪深股票日线行情
                        (jq_code         VARCHAR(10)      NOT NULL,
                        trade_date       DATE             NOT NULL,
                        open             NUMERIC          DEFAULT NULL,
                        close            NUMERIC          DEFAULT NULL,
                        low              NUMERIC          DEFAULT NULL,
                        high             NUMERIC          DEFAULT NULL,
                        volume           NUMERIC          DEFAULT NULL,
                        money            NUMERIC          DEFAULT NULL,
                        factor           NUMERIC          DEFAULT NULL,
                        high_limit       NUMERIC          DEFAULT NULL,
                        low_limit        NUMERIC          DEFAULT NULL,
                        avg              NUMERIC          DEFAULT NULL,
                        pre_close        NUMERIC          DEFAULT NULL,
                        paused           NUMERIC          DEFAULT NULL,
                        open_interest    NUMERIC          DEFAULT NULL,
                        PRIMARY KEY (ts_code, trade_date)
                            ) ; """
        return info

    def createTable(self,):
        sql_order = """CREATE    TABLE    沪深股票日线行情
                                        (jq_code         VARCHAR(50)      NOT NULL,
                                        trade_date       DATE             NOT NULL,
                                        open             NUMERIC          DEFAULT NULL,
                                        close            NUMERIC          DEFAULT NULL,
                                        low              NUMERIC          DEFAULT NULL,
                                        high             NUMERIC          DEFAULT NULL,
                                        volume           NUMERIC          DEFAULT NULL,
                                        money            NUMERIC          DEFAULT NULL,
                                        factor           NUMERIC          DEFAULT NULL,
                                        high_limit       NUMERIC          DEFAULT NULL,
                                        low_limit        NUMERIC          DEFAULT NULL,
                                        avg              NUMERIC          DEFAULT NULL,
                                        pre_close        NUMERIC          DEFAULT NULL,
                                        paused           NUMERIC          DEFAULT NULL,
                                        open_interest    NUMERIC          DEFAULT NULL,
                                        PRIMARY KEY (jq_code, trade_date)
                                            ) ; """
        if not (sql_order is None):
            self.cur.execute(sql_order)
        else:
            raise "table: 沪深股票日线行情 is exist!"
        print("Table created successfully")

    def deleleTable(self,):
        sql = ('drop table if exists 沪深股票日线行情;')
        self.cur.execute(sql)
        print(sql, "->Table deleted successfully")

    def insertInfo(self,start_date,end_date):
        #
        period_trade_date = jq.get_trade_days(start_date=start_date, end_date=end_date) # include start_date,end_date
        
        for data in period_trade_date:
            securities = jq.get_all_securities(types=[], date=data)
            df = jq.get_price(security = list(securities.index),start_date=start_date, end_date=end_date, frequency='daily', fields=fields, skip_paused=False, fq='pre', count=None, panel=False, fill_paused=False)
            #print (df)
            df = df.astype(object).where(pd.notnull(df), None)
            jq_code = df["code"]
            trade_date = df["time"]
            # open_p = df["open"].astype('float').where(pd.notnull(df), None)           
            # close_p = df["close"].astype('float').where(pd.notnull(df), None)
            # low_p = df["low"].astype('float').where(pd.notnull(df), None)
            # high_p = df["high"].astype('float').where(pd.notnull(df), None)
            # volume = df["volume"].astype('float').where(pd.notnull(df), None)
            # money = df["money"].astype('float').where(pd.notnull(df), None)
            # factor = df["factor"].astype('float').where(pd.notnull(df), None)
            # high_limit = df["high_limit"].astype('float').where(pd.notnull(df), None)
            # low_limit = df["low_limit"].astype('float').where(pd.notnull(df), None)
            # avg = df["avg"].astype('float').where(pd.notnull(df), None)
            # pre_close = df["pre_close"].astype('float').where(pd.notnull(df), None)
            # paused = df["paused"].astype('float').where(pd.notnull(df), None)
            # open_interest = df["open_interest"].astype('float').where(pd.notnull(df), None)

            open_p = df["open"].where(pd.notnull(df["open"]), None)           
            close_p = df["close"].where(pd.notnull(df["close"]), None)
            low_p = df["low"].where(pd.notnull(df["low"]), None)
            high_p = df["high"].where(pd.notnull(df["high"]), None)
            volume = df["volume"].where(pd.notnull(df["volume"]), None)
            money = df["money"].where(pd.notnull(df["money"]), None)
            factor = df["factor"].where(pd.notnull(df["factor"]), None)
            high_limit = df["high_limit"].where(pd.notnull(df["high_limit"]), None)
            low_limit = df["low_limit"].where(pd.notnull(df["low_limit"]), None)
            avg = df["avg"].where(pd.notnull(df["avg"]), None)
            pre_close = df["pre_close"].where(pd.notnull(df["pre_close"]), None)
            paused = df["paused"].where(pd.notnull(df["paused"]), None)
            open_interest = df["open_interest"].where(pd.notnull(df["open_interest"]), None)



            for i in range(len(jq_code)):
                            
                self.cur.execute("""
                            INSERT INTO 沪深股票日线行情 (jq_code, trade_date, open, close, low, high, volume, money,factor,high_limit,low_limit,avg,pre_close,paused,open_interest)
                            VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""",
                                        (jq_code[i],
                                        trade_date[i].strftime("%Y-%m-%d %H:%M:%S"),
                                        open_p[i],
                                        close_p[i],
                                        low_p[i],
                                        high_p[i],
                                        volume[i],
                                        money[i],
                                        factor[i],
                                        high_limit[i],
                                        low_limit[i],
                                        avg[i],
                                        pre_close[i],
                                        paused[i],
                                        open_interest[i]))
                self.con.commit()
            print("已插入日期：{0}，共有{1}天".format(data, len(period_trade_date)))
        
        print ("insert 沪深股票日线行情 from {} to {} finished!".format(start_date,end_date))


    def getPriceInfo(self,code,date,fields):
        