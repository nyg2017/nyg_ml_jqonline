import numpy as np
import jqdatasdk as jq
from util.jqdata_processor import list2Dic,dateArr2List,dataframe2Arr

#open  close   high    low       volume         money

open_idx = 0
close_idx = 1 
hight_idx = 2
low_idx = 3
volume_idx = 4
money_idx = 5


def getSortIndex(a):
    sorted_a = np.argsort(np.argsort(a))

    return sorted_a.astype(np.float)


def getReturnScore(base_price,future_price):
    _return = (future_price[:,close_idx] - base_price[:,close_idx]) / base_price[:,close_idx]
    mask = ~np.isnan(_return)
    score = np.full_like(_return,fill_value= np.nan)

    masked_return = _return[mask]

    sorted_return = getSortIndex(masked_return)

    _score = sorted_return / (sorted_return.shape[0]-1) - 0.5

    score[mask] = _score

    return score

def getPriceLeadingScore(stock_list,stock_index_dict,date_index_dict,inverse_date_index_dict,date,
                        #interval_list = [1,2,3,5,7,9,11,13,17],
                        #interval_weights = [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]):
                        interval_list = [1,20],
                        interval_weights = [1.0,1.0]):

    today_price = jq.get_price(stock_list, start_date=date, end_date=date, frequency='daily', fields=None, skip_paused=False, fq='pre', count=None, panel=False, fill_paused=True) 
    today_price = today_price.to_numpy()
    today_price_data = dataframe2Arr(today_price,stock_index_dict)

    return_score = []

    for i,interval in enumerate(interval_list):
        weight= interval_weights[i]
        befor_date = inverse_date_index_dict[date_index_dict[date] - interval]
        befor_price = jq.get_price(stock_list, start_date=befor_date, end_date=befor_date, frequency='daily', fields=None, skip_paused=False, fq='pre', count=None, panel=False, fill_paused=True)
        #print (befor_price)
        befor_price = befor_price.to_numpy()
        befor_price_data = dataframe2Arr(befor_price,stock_index_dict)
        score_i = getReturnScore(befor_price_data,today_price_data)

        return_score.append(score_i * interval_weights[i])
        
    return_score = np.array(return_score)

    return np.sum(return_score,axis=0)

    #return score
