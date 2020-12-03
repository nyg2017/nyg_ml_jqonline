import time
import datetime


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


def QA_util_stamp2datetime(timestamp):
    """
    explanation:
        datestamp转datetime,pandas转出来的timestamp是13位整数 要/1000,
        It’s common for this to be restricted to years from 1970 through 2038.
        从1970年开始的纳秒到当前的计数 转变成 float 类型时间 类似 time.time() 返回的类型
    
    params:
        * timestamp->
            含义: 时间戳
            类型: float
            参数支持: []
    
    return:
        datetime
    """
    try:
        return datetime.datetime.fromtimestamp(timestamp)
    except Exception as e:
        # it won't work ??
        try:
            return datetime.datetime.fromtimestamp(timestamp / 1000)
        except:
            try:
                return datetime.datetime.fromtimestamp(timestamp / 1000000)
            except:
                return datetime.datetime.fromtimestamp(timestamp / 1000000000)

    #


if __name__ == "__main__":
    date = "2020-01-12"
    a = QA_util_date_stamp(date)
    b = QA_util_stamp2datetime(a)
    print (b)