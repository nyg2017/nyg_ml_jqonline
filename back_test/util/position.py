import numpy as np 


def meanPosition(stock_rank):
    position = np.ones_like(stock_rank,dtype=np.float)
    position = position/np.sum(position)
    return position
    