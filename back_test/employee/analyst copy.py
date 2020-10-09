import pandas as pd
import tushare as ts
 
def get_annual_profit(maotai,geli,start_date,end_date):
    df_maotai=ts.get_hist_data(maotai,start=start_date,end=end_date)
    df_geli=ts.get_hist_data(geli,start=start_date,end=end_date)
    maotai_annual_profit=(1+(df_maotai.head(1)['close'].values[0]/df_maotai.tail(1)['close'].values[0]-1))**(250/df_maotai.shape[0])-1
    geli_annual_profit=(1+(df_geli.head(1)['close'].values[0]/df_geli.tail(1)['close'].values[0]-1))**(250/df_geli.shape[0])-1
    print u'茅台年化收益: ',maotai_annual_profit,u' 格力电器年化收益: ',geli_annual_profit
 
get_annual_profit('600519','000651','2017-06-01','2017-11-17')


import pandas as pd
import pymongo,datetime
import tushare as ts
import matplotlib as mpl
import matplotlib.pyplot as plt
 
conn = pymongo.MongoClient()
 
def get_sharp(fund_code):
    c=conn.stks.fund_codes.find_one({'code':fund_code})
    if c==None:
        return
    fund={
        'name':c['name'],
        'fund_id':c['_id'],
        'code':fund_code
    }
    df_fund=pd.DataFrame(list(conn.stks.fund_daily_values.find({
        'fund_id':fund['fund_id'],
        'date':{
            '$gte':datetime.datetime.strptime('2017-01-01','%Y-%m-%d'),
            '$lte':datetime.datetime.now()
        }
    })))
    df_fund.sort_values('date',ascending=True,inplace=True)
    df_fund['change']=df_fund['net_asset_value'].pct_change()
    
    annual_return=(df_fund['net_asset_value'].tail(1).values[0]/df_fund['net_asset_value'].head(1).values[0])**(250/df_fund.shape[0])-1
    lost_free_return=0.04
    sharp=(annual_return-lost_free_return)/df_fund['change'].describe().std()
    print fund['name']+' Sharp=',round(sharp*100,2),'%'
 
funds=['519195','110022','003095','001617','001195','502010','217027']
for f in funds:
    get_sharp(f)




13693089890
13693089890