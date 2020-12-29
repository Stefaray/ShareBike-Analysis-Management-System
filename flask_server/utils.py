from random import *
from DataBaseUtils.SqlUtil import OPMysql

def getRandomName():
    len=10
    name=""
    base1='A'
    base2='a'
    for i in range(len):
        if (randint(1, 2) % 2):
            name+=chr(ord(base1)+randint(0,25))
        else:
            name += chr(ord(base2) + randint(0, 25))
    return name

def genPhone():
    len=10
    phone="1"
    for i in range(len):
        phone+=str(randint(0,9))
    return phone

def genEmail():
    return getRandomName()+"@email.com"

def strfy(a):
    return '\''+a+'\''

def getRandomNum(len):
    num=""
    for i in range(len):
        num+=str(randint(1,10))
    return num

def query_sql(sql,parm=()):
    opsql = OPMysql()
    res = opsql.op_query(sql,parm)
    opsql.dispose()
    return res

def update_sql(sql,parm=()):
    opsql = OPMysql()
    cnt = opsql.op_update(sql,parm)
    opsql.dispose()
    return cnt

def update_sqllist(list):
    opsql=OPMysql()
    cnt = opsql.op_update_list(list)
    opsql.dispose()
    return cnt



from math import radians, cos, sin, asin, sqrt

'''计算公里数'''
def haversine(lon1, lat1, lon2, lat2):  # 经度1，纬度1，经度2，纬度2 （十进制度数）
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半径，单位为公里
    return c * r

