import pymysql
from model.bike import Bike
from datetime import datetime
from random import randint,random
from Global import *
import numpy as np


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

L=np.load("id.npz.npy").tolist()


# 打开数据库连接
db = pymysql.connect("rm-uf6qd27273l97cho1eo.mysql.rds.aliyuncs.com", "root", "123456aa", "sharebike")

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

for i in L:
    print(i)
    bike=Bike(i,datetime(2006,1,10,randint(1,20),randint(1,50),0),BikeStatus.Idle,random()*5+116,random()*10+30)
    sql='''INSERT INTO bike VALUES(%d,%s,%d,%f,%f)'''%(
        bike.bikeid,strfy(str(bike.prod_time)),bike.status.value,bike.location_x,bike.location_y
    )
    # 执行sql语句
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()

# 关闭数据库连接
db.close()


