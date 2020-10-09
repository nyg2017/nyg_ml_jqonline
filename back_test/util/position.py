import numpy as np 


def standardization(data):
    mu = np.mean(data, axis=0)
    sigma = np.std(data, axis=0)
    return (data - mu) / sigma

def meanPosition(stock_score):
    position = np.ones_like(stock_score,dtype=np.float)
    position = position/np.sum(position)
    return position

def expPosition(stock_score):
    stock_exp = np.exp(standardization(stock_score))
    position = stock_exp/ np.sum(stock_exp)
    return position

    