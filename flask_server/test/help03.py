import pymysql
from model.user import User
from datetime import datetime
from random import *
from Global import *


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

# 打开数据库连接
db = pymysql.connect("rm-uf6qd27273l97cho1eo.mysql.rds.aliyuncs.com", "root", "123456aa", "sharebike")

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

'''0~1037'''
user=User(20000,datetime.now(),
              'jack',"123456",Identity.admin,phone='18321955399',money=1000,email='957947142@qq.com')
sql='''insert ignore into user(userid,register_date,username,password,identity,phone,email,money) values(%d,
%s,%s,%s,%d,%s,%s,%d)'''%(user.userid,strfy(str(user.register_date)),strfy(user.username),strfy(user.password),user.identity.value,
                          strfy(user.phone)
                          ,strfy(user.email),user.money)

# 执行sql语句
cursor.execute(sql)
# 提交到数据库执行
db.commit()
# print("成功插入一条")
# 如果发生错误则回滚




# 关闭数据库连接
db.close()