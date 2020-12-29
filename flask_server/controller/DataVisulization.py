from datetime import *

from utils import *
from Global import *
from flask import request,session
from flask_cors import CORS
import json

'''1公里约等于0.009度'''
uintMiles=0.009

CORS(dataBlueprint)

@dataBlueprint.route("/dataByAreaAndTime", methods=['POST'])
def Riding_Data_By_Area_And_Time():
    '''
    说明
        根据东北和西南的经纬度确定一个地区，再给一个诸如7：00~8：00的时间段，
        给出符合该要求的所有骑行数据
        骑行数据为订单的数据
    参数
        NorthEast_location:{"x":,"y":} x除了两条116，其余全是121.xxx， y除了两条是40，其余全是31.xxx
        SouthWest_location:{"x":,"y":} x的取值范围在116~121左右， y的取值范围在30~40，和上面类似
        time：{"first":7,"second": 8} 注意 first 和 second 的参数是整数 0~23
    :return:
        return {"res":res}
    '''
    NorthEast_location = request.form['NorthEast_location']
    print(NorthEast_location)
    SouthWest_location = request.form['SouthWest_location']
    time=request.form['time']
    NorthEast_location=json.loads(NorthEast_location)
    SouthWest_location=json.loads(SouthWest_location)
    time=json.loads(time)
    time["first"]=PinChou(time["first"])
    time["second"] = PinChou(time["second"])
    sql="select * from order_table where "
    sql = sql + " start_location_x > "+str(SouthWest_location["x"])+" and start_location_x <"+str(NorthEast_location["x"])+" "
    sql = sql + "and  start_location_y > "+str(NorthEast_location["y"])+" and start_location_y <"+str(SouthWest_location["y"])+" "
    sql=sql+" and DATE_FORMAT(start_time,'%%H:%%i:%%S')>="+strfy(time["first"])+" AND DATE_FORMAT(start_time,'%%H:%%i:%%S')<"+strfy(time["second"])+" "
    print(sql)
    res=query_sql(sql)
    return {"res":res}


@dataBlueprint.route("/queryDayChangeByArea", methods=['POST'])
def query_Day_Change_By_Area():
    '''
    说明
        给定一个地区和一对日期，如’2020-08-01‘，’2020-08-05‘
        返回该地区每天订单数随时间的变化情况
    参数
        NorthEast_location:{"x":121.6,"y":31.23} x除了两条116，其余全是121.xxx， y除了两条是40，其余全是31.xxx
        SouthWest_location:{"x":121.33,"y":31.33} x的取值范围在116~121左右， y的取值范围在30~40，和上面类似
        date：{"first":"2016-08-01","second": "2016-08-05"}
    :return:
        return {"map":datamap}
    '''
    NorthEast_location = request.form['NorthEast_location']
    SouthWest_location = request.form['SouthWest_location']
    date = request.form['date']
    NorthEast_location = json.loads(NorthEast_location)
    SouthWest_location = json.loads(SouthWest_location)
    date = json.loads(date)

    d1=datetime.strptime(date["first"], '%Y-%m-%d')
    d2=datetime.strptime(date["second"], '%Y-%m-%d')
    datamap=dict()
    while(d1.timestamp()<=d2.timestamp()):
        variable=[d1.timestamp(),d1.timestamp(),SouthWest_location["x"],NorthEast_location["x"],NorthEast_location["y"],SouthWest_location["y"]]
        sql="SELECT COUNT(*) as cnt FROM order_table WHERE UNIX_TIMESTAMP(start_time) BETWEEN %s AND %s+86399 "
        sql = sql + " and start_location_x > %s and start_location_x <%s "
        sql = sql + " and  start_location_y > %s and start_location_y <%s "
        res=query_sql(sql,tuple(variable))[0]["cnt"]
        datamap[d1.strftime('%Y-%m-%d')]=res
        d1+=timedelta(days=1)
    return {"map":datamap}


def PinChou(num):
    base=''
    if(len(str(num))==1):
        base='0'+str(num)
    else:
        base=str(num)
    return base+":00:00"

@dataBlueprint.route("/queryHourChangeByArea", methods=['POST'])
def query_Hour_Change_By_Area():
    '''
    说明
        给定一个地区和一对时间段，如’7:00:00‘，’20:00:00‘
        返回该地区每一个小时订单数随时间的变化情况
    参数
        NorthEast_location:{"x":121.6,"y":31.23} x除了两条116，其余全是121.xxx， y除了两条是40，其余全是31.xxx
        SouthWest_location:{"x":121.33,"y":31.33} x的取值范围在116~121左右， y的取值范围在30~40，和上面类似
        time：{"first":7,"second": 20} 注意 first 和 second 的参数是整数 0~23
    :return:
        return {"map": datamap}
    '''
    NorthEast_location = request.form['NorthEast_location']
    SouthWest_location = request.form['SouthWest_location']
    time = request.form['time']
    NorthEast_location = json.loads(NorthEast_location)
    SouthWest_location = json.loads(SouthWest_location)
    time = json.loads(time)
    t1=time["first"]
    t2=time["second"]
    datamap = dict()
    while (t1<t2):
        variable = [PinChou(t1), PinChou(t1+1), SouthWest_location["x"], NorthEast_location["x"],
                    NorthEast_location["y"], SouthWest_location["y"]]
        sql = "SELECT COUNT(*) as cnt FROM order_table WHERE DATE_FORMAT(start_time,'%%H:%%i:%%S')>=%s AND DATE_FORMAT(start_time,'%%H:%%i:%%S')<%s "
        sql = sql + " and start_location_x > %s and start_location_x <%s "
        sql = sql + " and  start_location_y > %s and start_location_y <%s "
        res = query_sql(sql, tuple(variable))[0]["cnt"]
        datamap[PinChou(t1)+"~"+PinChou(t1+1)] = res
        t1+=1
    return {"map": datamap}

@dataBlueprint.route("/queryBikesByPointAndRadius/<r>", methods=['POST'])
def query_Bikes_By_Point_And_Radius(r):
    '''
    说明
        根据一个经纬度和半径，返回所有的单车数据，单车数据包括位置和状态
        锁定闲置状态为0
        骑行状态为1
        每一辆单车的初始位置都是随机生成
        例子：经度120.627258，纬度31.43
    query参数
        location :{"x":121.05,"y":31.54}  x代表经度， y代表维度
    :param r:半径 ，单位公里
    :return:
         return {"res":res}
    '''
    location=request.form['location']
    location=json.loads(location)
    x=(location["x"])
    y=(location["y"])
    r=eval(r)
    # print(type(x))
    small={"x":x-r*uintMiles,"y":y-r*uintMiles}
    big={"x":x+r*uintMiles,"y":y+r*uintMiles}
    res=query_sql("select * from bike where location_x between %s and %s and location_y between %s and %s",
              (small["x"],big["x"],small["y"],big["y"]))
    # print(len(res))
    return {"res":res}


    

@dataBlueprint.route("/listDataByAreaAndTime", methods=['POST'])
def List_Data_By_Area_And_Time():
    '''
    说明
        给定一组地区 和 一个时间段，返回骑车数据
        参数：
            -list 每一个item的格式
                -NorthEast_location:{"x":,"y":} x除了两条116，其余全是121.xxx， y除了两条是40，其余全是31.xxx
                -SouthWest_location:{"x":,"y":} x的取值范围在116~121左右， y的取值范围在30~40，和上面类似
                示例: [{"NorthEast_location": {"x": 121.5, "y": 31.4}, "SouthWest_location": {"x": 121.3, "y": 31.5}}, {"NorthEast_location": {"x": 121.8, "y": 31.1}, "SouthWest_location": {"x": 121.5, "y": 31.3}}]
                示例结束
            -time：{"first":7,"second":8} 注意 first 和 second 的参数是整数 0~23

    :return:
        return {"list": resL}
    '''
    # list=request.form["list"]
    # list=json.loads(list)
    resL=[]
    time = request.form["time"]
    time=json.loads(time)
    # for item in list:
    #     NorthEast_location = item['NorthEast_location']
    #     SouthWest_location = item['SouthWest_location']
    #     sql = "select * from order_table where "
    #     sql = sql + " start_location_x > %s and start_location_x <%s "
    #     sql = sql + "and  start_location_y > %s and start_location_y <%s "
    #     sql = sql + " and DATE_FORMAT(start_time,'%%H:%%i:%%S')>=%s AND DATE_FORMAT(start_time,'%%H:%%i:%%S')<=%s "
    #     variable = [SouthWest_location["x"], NorthEast_location["x"], NorthEast_location["y"], SouthWest_location["y"],
    #                 time["first"], time["second"]]
    #     res = query_sql(sql, tuple(variable))
    #     resL.append(res)
    sql = "select * from order_table where "
    sql = sql + " DATE_FORMAT(start_time,'%%H:%%i:%%S')>=%s AND DATE_FORMAT(start_time,'%%H:%%i:%%S')<=%s "
    variable = [time["first"], time["second"]]
    res = query_sql(sql, tuple(variable))
    resL.append(res)
    return {"list": resL}




