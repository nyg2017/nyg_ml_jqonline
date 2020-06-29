import numpy as np
import pandas as pd
import datetime
import os


def list2Dic(in_list):
    index_list = [i for i in range(len(in_list))]
    return dict(zip(in_list,index_list))

def invert_dict(d):
    return dict(zip(d.values(), d.keys()))

def dateArr2List(date_arr):
    date_list = [pd.Timestamp(date) for date in date_arr]
    return date_list





def dataframe2Arr(prince_info,stock_index_dict,date_index_dict=None):
    
    if date_index_dict == None:
        price_data = np.full((len(stock_index_dict),prince_info.shape[1]-2),fill_value = np.nan)
        for d in prince_info:
            day = d[0]
            stock = d[1]
            idx_2 = stock_index_dict[stock]
            price_data[idx_2] = d[2:]
    else:
        price_data = np.full((len(date_index_dict),len(stock_index_dict),prince_info.shape[1]-2),fill_value = np.nan)

        for d in prince_info:
            day = d[0]
            stock = d[1]
            idx_1 = date_index_dict[day]
            idx_2 = stock_index_dict[stock]
            price_data[idx_1][idx_2] = d[2:]
    return price_data

def process_jqdata(index_dic,data_path,save_dir):
    processe_day = datetime.datetime.now().strftime('%Y-%m-%d')
    save_dir = os.path.join(save_dir,processe_day)
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    data = pd.read_csv(data_path)
    columns = data.columns.values

    code_idx_dic = index_dic
    index_1 = len(index_dic)
    '''
    code_idx_dic = {}
    index_1 = 0
    for i , name in enumerate(data.minor):
        if name not in code_idx_dic.keys():
            code_idx_dic[name] = index_1
            index_1 +=1
    '''

    days_idx_dic = {}
    index_2 = 0
    for i , name in enumerate(data.major):
        if name not in days_idx_dic.keys():
            days_idx_dic[name] = index_2
            index_2 +=1

    data = data.to_numpy()
    
    re_data = np.full((index_2,index_1,data.shape[1]-2),fill_value = np.nan)
    for d in data:
        day = d[0]
        stock = d[1]
        idx_1 = days_idx_dic[day]
        idx_2 = code_idx_dic[stock]
        re_data[idx_1][idx_2] = d[2:]
    
    print ("stocks num:", index_1)
    print ("days nums:", index_2)
    
    save_columns = columns[2:]
    for i,column in enumerate(save_columns):
        save_path = os.path.join(save_dir,column + ".npy")
        np.save(save_path,re_data[:,:,i])

