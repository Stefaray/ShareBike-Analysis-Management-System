import pymysql
from DBUtils.PooledDB import PooledDB

class OPMysql(object):

    __pool = None

    def __init__(self):
        # 构造函数，创建数据库连接、游标
        self.coon = OPMysql.getmysqlconn()
        self.cur = self.coon.cursor(cursor=pymysql.cursors.DictCursor)


    # 数据库连接池连接
    @staticmethod
    def getmysqlconn():
        if OPMysql.__pool is None:
            __pool = PooledDB(creator=pymysql, mincached=1, maxcached=20, host=mysqlInfo['host'], user=mysqlInfo['user'], passwd=mysqlInfo['passwd'], db=mysqlInfo['db'], port=mysqlInfo['port'], charset=mysqlInfo['charset'])
        return __pool.connection()

    # 插入\更新\删除sql
    def op_update(self, sql,param):
        # print('op_insert', sql)
        insert_num = self.cur.execute(sql,param)
        # print('mysql sucess ', insert_num)
        self.coon.commit()
        return insert_num

    # 查询
    def op_query(self, sql,parm):
        # print('op_select', sql)
        self.cur.execute(sql,parm)  # 执行sql
        select_res = self.cur.fetchall()  # 返回结果为字典
        # print('op_select', select_res)
        return select_res

    def op_update_list(self,list):
        sum=0
        try:
            for tuple in list:
                sql,parm=tuple
                insert_num = self.cur.execute(sql, parm)
                if(insert_num==0):
                    self.coon.rollback()
                    break
                sum+=insert_num
            self.coon.commit()
        except:
            print('事务回滚')
            self.coon.rollback()
        return sum
    #释放资源
    def dispose(self):
        self.coon.close()
        self.cur.close()

mysqlInfo = {
    "host": 'rm-uf6qd27273l97cho1eo.mysql.rds.aliyuncs.com',
    "user": 'root',
    "passwd": '123456aa',
    "db": 'sharebike',
    "port": 3306,
    "charset": 'utf8mb4'
}




