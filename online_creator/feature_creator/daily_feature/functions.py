


def var(date,params_list,stock_list,date_index_dict,inverse_date_index_dict,price_buffer,query_and_buffer):

    #base_price = query_and_buffer(date,stock_list,price_buffer)
    
    for var in params_list:
        date_index = date_index_dict[date]
        base_date = inverse_date_index_dict[date_index - var-1]
        future_date = inverse_date_index_dict[date_index - var]
        base_price = query_and_buffer(base_date,stock_list,price_buffer)
        future_price = query_and_buffer(future_date,stock_list,price_buffer)
        print (base_price,future_price)

def return_n_day(date,value_list,stock_listdate_index_dict):
    pass

def high_d_close(date,value_list,stock_listdate_index_dict):

    pass