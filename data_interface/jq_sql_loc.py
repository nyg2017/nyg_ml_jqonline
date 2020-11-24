import psycopg2


class SqlJqData(object):
    def __init__(self,database="postgres",\
                user="postgres",
                password="123456",
                host="127.0.0.1",
                port="5432"):
        self.con = psycopg2.connect(database=database, user=user, password=password, host=host, port=port) 
        self.cur = con.cursor()

    def createTable(self,sql_order = None):
        sql_order = """CREATE    TABLE    沪深300指数日线行情
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
        if sql_order not None:
            cur.execute(sql_order)

        print("Table created successfully")

    def deleteTable(self,table_name):
        sql = ('drop table if exists %s;'% table_name)
        cur.execute(sql)
        print(sql, "->Table deleted successfully")


    def insertData(self,infos):
        table_name = infos["table_name"]
        
        cur.execute("""
                    INSERT INTO 沪深300指数日线行情 (jq_code, trade_date, open, high_p, low_p, close_p, pre_close, pct_chg)
                    VALUES( %s, %s, %s, %s, %s, %s, %s, %s);""",
                                (ts_code[i],
                                trade_date[i],
                                open_p[i],
                                high_p[i],
                                low_p[i],
                                close_p[i],
                                pre_close[i],
                                pct_chg[i]))
        con.commit()
        print("已插入{0}行，共有{1}行".format(count, len(ts_code)))

if __name__ == "__main__":
    #login()
    createTabel()