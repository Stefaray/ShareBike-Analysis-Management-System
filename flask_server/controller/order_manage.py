from utils import *
from Global import *
from flask import request,session
import datetime
import time
import math
import json
import pytz
from datetime import datetime

# 显示所有订单列表
@orderBlueprint.route("/order_table", methods=['POST'])
def order_table():
    returnmsg = []
    params = request.form["query"]
    print(params)
    
    param = json.loads(params)  
    
    
    page  = param["page"]
    limit = param["limit"]
    least_piece = (page - 1) * limit
    # max_piece = page * limit
    title = param["title"]
    importance = str(param["importance"])
    if(importance == '订单ID'):
        importance = 'orderid'
    elif(importance == '单车ID'):
        importance = 'bikeid'
    elif(importance == '用户ID'):
        importance = 'userid'
    elif(importance == '开始时间'):
        importance = 'start_time'
    elif(importance == '结束时间'):
        importance = 'end_time'
    elif(importance == '起始点经度'):
        importance = 'start_location_x'
    elif(importance == '起始点纬度'):
        importance = 'start_location_y'
    elif(importance == '结束点经度'):
        importance = 'end_location_x'
    elif(importance == '结束点纬度'):
        importance = 'end_location_y'
    

    if(title != ''):
        print(importance)
        print(title)
        print(str(least_piece) +'-------------------')
        # cursor.execute('Select * From order_table Where '+ importance +' like \'%'+title+'%\' limit ' + str(least_piece) + ', ' + str(limit) )
        result = query_sql('Select * From order_table Where '+ importance +' like \'%'+title+'%\' limit ' + str(least_piece) + ', ' + str(limit))
        # print(result)
        total = query_sql('Select count(*) as num From order_table Where '+ importance +' like \'%'+title+'%\'')


        # print(total)
    # cursor = pymysql.cursors.SSCursor(connectDB)
    else:
        result = query_sql('Select * From order_table LIMIT ' + str(least_piece) + ', ' + str(limit) )
        # result = cursor.fetchall()
        total = query_sql('Select count(*) as num From order_table')
        # total = cursor.fetchall()
    
    total = total[0]["num"]
    returnmsg={"code":20000,"desc":"UID接收成功","items":result,"total":total}


    return returnmsg


# 增加订单
@orderBlueprint.route("/order_ADD",methods=["POST"])
def order_ADD():
    returnmsg = []
    params = request.form["data"]
    print(params)
    
    param = json.loads(params)
    bikeid = str(param["bikeid"])
    userid = str(param["userid"])
    start_location_x = str(param["start_location_x"])
    start_location_y = str(param["start_location_y"])
    end_location_x = str(param["end_location_x"])
    end_location_y  = str(param["end_location_y"])
    start_time = param["start_time"]
    end_time = param["end_time"]
    track = str(param["track"])

    end_time = utc_to_local(end_time, utc_format='%Y-%m-%dT%H:%M:%S.%fZ')
    ltime=time.localtime(end_time)  
    end_time=time.strftime("%Y-%m-%d %H:%M:%S", ltime)

    start_time = utc_to_local(start_time, utc_format='%Y-%m-%dT%H:%M:%S.%fZ')
    ltime=time.localtime(start_time)  
    start_time=time.strftime("%Y-%m-%d %H:%M:%S", ltime)
    print(start_time)

    orderid = int(time.time())
    orderid = str(orderid)
    print( '---------------------------------------')
    # update_sql("select userid from user where username=%s",(username))[0]["userid"]
    update_sql('Insert   order_table (orderid,bikeid,userid,start_location_x,start_location_y,end_location_x,end_location_y,start_time,end_time,track)  VALUES('
                   + orderid + ',' + bikeid + ',' + userid + ',' + start_location_x + ',' + start_location_y + ',' + end_location_x 
                    + ',' + end_location_y + ',"' + str(start_time) + '","' + str(end_time) + '","' + track + '" ) ')

    # total = query_sql('Select total_order From total Where id = 0')
    # new_total = total[0]["total_order"] + 1
    # update_sql('Update total Set total_order = '+str(new_total)+' Where id = 0')

    returnmsg={"code":20000,"desc":"UID接收成功","orderid":orderid}
    return returnmsg


# UTCS时间转换为时间戳 2018-07-13T16:00:00Z
def utc_to_local(utc_time_str, utc_format='%Y-%m-%dT%H:%M:%SZ'):
    local_tz = pytz.timezone('Asia/Chongqing')      #定义本地时区
    local_format = "%Y-%m-%d %H:%M:%S"              #定义本地时间format

    utc_dt = datetime.strptime(utc_time_str, utc_format)       #讲世界时间的格式转化为datetime.datetime格式
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)     #想将datetime格式添加上世界时区，然后astimezone切换时区：世界时区==>本地时区
    #time_str = local_dt.strftime(local_format)                         #将datetime格式转化为str—format格式
    #return int(time.mktime(time.strptime(time_str, local_format)))     #运用mktime方法将date—tuple格式的时间转化为时间戳;time.strptime()可以得到tuple的时间格式
    return int(time.mktime(local_dt.timetuple()))                       #返回当地时间戳


# 更新编辑订单
@orderBlueprint.route("/order_UPDATE",methods=["POST"])
def order_UPDATE():
    returnmsg = []
    params = request.form["data"]
    print(params)
    
    param = json.loads(params)
    orderid = str(param["orderid"])
    bikeid = str(param["bikeid"])
    userid = str(param["userid"])
    start_location_x = str(param["start_location_x"])
    start_location_y = str(param["start_location_y"])
    end_location_x = str(param["end_location_x"])
    end_location_y  = str(param["end_location_y"])
    start_time = param["start_time"]
    end_time = param["end_time"]
    track = str(param["track"])
    # end_time = utc_to_local(end_time, utc_format='%a, %d %b %Y %H:%M:%S GMT')   
    # # end_time = utc_to_local(end_time, utc_format='%a, %d %b %Y %H:%M:%S GMT')
    # ltime=time.localtime(end_time)  
    # end_time=time.strftime("%Y-%m-%d %H:%M:%S", ltime)


    # start_time = utc_to_local(start_time, utc_format='%a, %d %b %Y %H:%M:%S GMT')
    # ltime=time.localtime(start_time)  
    # start_time=time.strftime("%Y-%m-%d %H:%M:%S", ltime)

    end_time = utc_to_local(end_time, utc_format='%Y-%m-%dT%H:%M:%S.%fZ')
    ltime=time.localtime(end_time)  
    end_time=time.strftime("%Y-%m-%d %H:%M:%S", ltime)

    start_time = utc_to_local(start_time, utc_format='%Y-%m-%dT%H:%M:%S.%fZ')
    ltime=time.localtime(start_time)  
    start_time=time.strftime("%Y-%m-%d %H:%M:%S", ltime)


    # cursor.execute('Update order_table Set bikeid="'+bikeid+'",userid='+userid+' where orderid = ' + orderid ) 
    update_sql('Update order_table Set bikeid='+bikeid+',userid='+userid+',start_location_x='+start_location_x+',start_location_y='+start_location_y+
                    ',end_location_x='+end_location_x+',end_location_y='+end_location_y+',start_time="'+start_time+'",end_time="'+end_time+'",track="'+track+'" Where orderid = ' + orderid) 


    returnmsg={"code":20000,"desc":"UID接收成功","orderid":1}
    return returnmsg


# 删除订单
@orderBlueprint.route("/order_DELETE",methods=["POST"])
def order_DELETE():
    returnmsg = []
    params = request.form["data"]
    print(params)
    param = json.loads(params)
    orderid = str(param["orderid"])


    # print( '---------------------------------------')

    update_sql('Delete From order_table Where orderid = ' + orderid ) 

    

    returnmsg={"code":20000,"desc":"UID接收成功","orderid":1}
    return returnmsg

##  正在骑行订单后端 ##
# 显示列表
@orderBlueprint.route("/going_order", methods=['POST'])
def going_order():  
    returnmsg = []
    params = request.form["query"]
    print(params)
    
    param = json.loads(params)  
    
    
    page  = param["page"]
    limit = param["limit"]
    least_piece = (page - 1) * limit
    # max_piece = page * limit
    title = param["title"]
    importance = str(param["importance"])
    if(importance == '订单ID'):
        importance = 'bindid'
    elif(importance == '单车ID'):
        importance = 'bikeid'
    elif(importance == '用户ID'):
        importance = 'userid'
    elif(importance == '开始时间'):
        importance = 'start_time'
    elif(importance == '起始点经度'):
        importance = 'start_location_x'
    elif(importance == '起始点纬度'):
        importance = 'start_location_y'

    

    if(title != ''):
        print(importance)
        print(title)
        print(str(least_piece) +'-------------------')
        
        result = query_sql('Select * From bind Where '+ importance +' like \'%%'+title+'%%\' limit ' + str(least_piece) + ', ' + str(limit))
        print(result)
        total = query_sql('Select count(*) as num From bind Where '+ importance +' like \'%%'+title+'%%\'')


        # print(total)
    # cursor = pymysql.cursors.SSCursor(connectDB)
    else:
        result = query_sql('Select * From bind LIMIT ' + str(least_piece) + ', ' + str(limit) )
        # result = cursor.fetchall()
        total = query_sql('Select count(*) as num From bind')
        # total = cursor.fetchall()
    
    total = total[0]["num"]
    returnmsg={"code":20000,"desc":"UID接收成功","items":result,"total":total}
    return returnmsg
    

@orderBlueprint.route("/addGoingOrder", methods=['POST'])
def add_Going_Order():  
    '''
    说明
        增加一条正在进行的订单
    参数
        username String类型
        bikeid bigint类型
        start_location_x  double类型
        start_location_y  double类型
    :return:
        -成功
            return {"msg":'新增成功',"bike":goingOrder}
    '''
    params = request.form["data"]
    param = json.loads(params)
    username=param['username']

    bikeid=param['bikeid']
    print(type(bikeid))

    user_cnt=len(query_sql('select * from user where username=%s',(username)))
    bike_cnt=len(query_sql('select * from bike where bikeid=%s', (bikeid)))
    if(user_cnt==0 or bike_cnt==0):
        return '请输入正确的username或bikeid'
    start_time=datetime.now()
    start_location_x=param['start_location_x']
    start_location_y=param['start_location_y']


    userid = query_sql("select userid from user where username=%s",(username))[0]["userid"]
    userid = str(userid)
    print(type(userid))
    # print(userid)
    # 转换为userid
    cnt=update_sql("INSERT INTO bind(userid,bikeid,start_time,start_location_x,start_location_y) "
               "VALUES(%s,%s,%s,%s,%s)",(userid,bikeid,start_time,start_location_x,start_location_y))

    update_sql('update bike set status=%s where bikeid=%s',(BikeStatus.Riding.value,bikeid))
    
    goingOrder=query_sql("select * from bind where userid=%s",(userid))[0]
    print(going_order)
    if(cnt==1):
        return {"msg":'新增成功',"bind":goingOrder}
    else:
        return '新增失败'


@orderBlueprint.route("/addTrackPoint")
def add_Tract_Point():
    '''
    说明
        当一个订单正在进行时，插入新的轨迹点，
    参数
        bindid 正在进行订单的id
        newPoint  例如 '121.54,30.96' 格式是字符串，两个坐标逗号分隔
    :return:
        -成功
            return {"msg":'插入成功',"bind":bind}
    '''
    bindid=request.args.get('bindid')
    newPoint=request.args.get('newPoint')
    bind=query_sql("select * from bind where bindid=%s",(bindid))[0]
    if (bind["track"] == None):
        bind["track"] = ''
    print(bind["track"],newPoint)
    new_track=bind["track"]+"#"+newPoint
    cnt=update_sql("update bind set track=%s where bindid=%s",(new_track,bindid))

    bind["track"]=new_track
    if(cnt==1):
        return {"msg":'插入成功',"bind":bind}
    return '插入失败'


@orderBlueprint.route("/endGoingOrder",methods=["POST"])
def end_Going_Order():
    '''
    说明
        结束一个正在进行的订单，同时将该单车的状态置为闲置，并增加一条已结束订单
    参数
        bindid 整数
        end_location_x 浮点数
        end_location_y 浮点数
    :return:
        -成功
           '结束订单成功'
    '''
    params = request.form['data']
    param = json.loads(params)
    bindid=          str(param['bindid'])
    end_location_x = str(param['end_location_x'])
    end_location_y = str(param['end_location_y'])
    bind=query_sql("select * from bind where bindid=%s",(bindid))[0]
    print(bind)
    end_time=datetime.now()
    # sql,pram=("insert into order_table(bikeid,userid,"
    #                "start_time,start_location_x,start_location_y,"
    #                "end_time,end_location_x,end_location_y,track)"
    #                " values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(bind["bikeid"],bind["userid"],bind["start_time"],
    #                                                       bind["start_location_x"],bind["start_location_y"],
    #                                                       end_time,end_location_x,end_location_y,bind["track"]))
    update_sql("insert into order_table(bikeid,userid,"
                   "start_time,start_location_x,start_location_y,"
                   "end_time,end_location_x,end_location_y,track)"
                   " values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(bind["bikeid"],bind["userid"],bind["start_time"],
                                                          bind["start_location_x"],bind["start_location_y"],
                                                          end_time,end_location_x,end_location_y,bind["track"]))
    # List=[]
    # List.append((sql,pram))
    update_sql('update bike set status=%s and location_x=%s and location_y=%s where bikeid=%s', \
             (BikeStatus.Idle.value, end_location_x,end_location_y,bind["bikeid"]))
    # sql,pram='update bike set status=%s and location_x=%s and location_y=%s where bikeid=%s', \
    #          (BikeStatus.Idle.value, end_location_x,end_location_y,bind["bikeid"])
    # List.append((sql,pram))
    # sql,pram="delete from bind where bindid=%s", (bindid)
    # List.append((sql, pram))
    # print(List)
    # cnt=update_sqllist(List)
    cnt = update_sql("delete from bind where bindid=%s", (bindid))
    print(cnt)
    if(cnt<3):
        return '结束订单失败'
    return '结束订单成功'

@orderBlueprint.route("/delOrder")
def del_Order():
    '''
    说明
        删除一个已结束的订单
    参数
        orderid
    :return:
        -成功
            '删除成功'
    '''
    orderid=request.args.get('orderid')
    orders=query_sql('select * from order_table where orderid=%s' ,(orderid))
    if(len(orders)==0):
        return 'orderid有误'
    cnt=update_sql('delete from order_table where orderid=%s',(orderid))
    if(cnt>0):
        return '删除成功 '
    return '删除失败'


@orderBlueprint.route('/addOrder')
def add_Order():
    '''
    说明
        增加一个已结束的订单
    参数
        bikeid 整数
        userid 整数
        start_time 日期 格式‘2020-06-06 17:55:55’
        start_location_x 浮点数
        start_location_y 浮点数
        end_time
        end_location_x
        end_location_y
        track 字符串
    :return:
        - 成功
            return {"msg":"成功","order":order}
    '''
    userid = request.args.get('userid')
    bikeid = request.args.get('bikeid')

    user_cnt = len(query_sql('select * from user where userid=%s', (userid)))
    bike_cnt = len(query_sql('select * from bike where bikeid=%s', (bikeid)))
    if (user_cnt == 0 or bike_cnt == 0):
        return '请输入正确的userid或bikeid'
    start_time = request.args.get('start_time')
    start_location_x = request.args.get('start_location_x')
    start_location_y = request.args.get('start_location_y')
    end_time=request.args.get('end_time')
    end_location_x=request.args.get('end_location_x')
    end_location_y=request.args.get('end_location_y')
    track=request.args.get('track')

    maxid=query_sql('select max(orderid) as maxid from order_table')[0]["maxid"]
    orderid=maxid+1
    cnt=update_sql('insert into order_table(orderid,bikeid,userid,start_time,start_location_x,start_location_y,'
               'end_time,end_location_x,end_location_y,track)'
               ' values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(orderid,bikeid,userid,start_time,start_location_x,
                                                         start_location_y,end_time,end_location_x,end_location_y,track))
    if(cnt>0):
        order=query_sql("select * from order_table where orderid=%s",(orderid))[0]
        return {"msg":"成功","order":order}
    return '删除失败'


@orderBlueprint.route('/editOrder')
def edit_Order():
    '''
    说明
        修改订单的一些信息
    参数
        orderid 整数
        bikeid 整数
        userid 整数
        start_time 日期 格式‘2020-06-06 17:55:55’
        start_location_x 浮点数
        start_location_y 浮点数
        end_time
        end_location_x
        end_location_y
        track 字符串
    :return:
        -成功
            {"msg": "成功", "order": order}
    '''
    orderid=request.args.get('orderid')
    userid = request.args.get('userid')
    bikeid = request.args.get('bikeid')
    start_time = request.args.get('start_time')
    start_location_x = request.args.get('start_location_x')
    start_location_y = request.args.get('start_location_y')
    end_time = request.args.get('end_time')
    end_location_x = request.args.get('end_location_x')
    end_location_y = request.args.get('end_location_y')
    track = request.args.get('track')
    cnt = update_sql('update order_table set bikeid=%s , userid=%s , start_time=%s , '+
                     'start_location_x=%s , start_location_y=%s ,'+
                     ' end_time=%s , end_location_x=%s , end_location_y=%s , track=%s where orderid=%s',
                     ( bikeid, userid, start_time, start_location_x,
                      start_location_y, end_time, end_location_x,end_location_y, track,orderid))

    if(cnt==0):
        return '修改失败'
    order = query_sql("select * from order_table where orderid=%s", (orderid))[0]
    return {"msg": "成功", "order": order}


@orderBlueprint.route("/getOrdersByPage/<int:page>/<int:cntPerPage>")
def get_Orders_By_Page(page,cntPerPage):
    '''
    :param page: 代表页数 从1开始 整数
    :param cntPerPage: 每一页有多少条数据 整数
    说明
        按页码获得相应的已结束订单

    :return:
        return {'res':res}
    '''
    skip=(page-1)*cntPerPage
    res=query_sql("select * from order_table limit %s,%s",(skip,cntPerPage))
    return {'res':res}

@orderBlueprint.route("/getBindsByPage/<int:page>/<int:cntPerPage>")
def get_Binds_By_Page(page,cntPerPage):
    '''
    :param page: 代表页数 从1开始 整数
    :param cntPerPage: 每一页有多少条数据 整数
    说明
        按页码获得相应的正在进行订单

    :return:
        {"bind":bind_cnt,"order":order_cnt}
    '''
    skip=(page-1)*cntPerPage
    res=query_sql("select * from bind limit %s,%s",(skip,cntPerPage))
    return {'res':res}

@orderBlueprint.route("/getCount")
def get_Orders_Count():
    '''
    获得所有的已结束的订单数量和正在进行的订单数量
    :return:
    '''
    bind_cnt=query_sql("select count(*) as cnt from bind")[0]["cnt"]
    order_cnt=query_sql("select count(*) as cnt from order_table")[0]["cnt"]
    return {"bind":bind_cnt,"order":order_cnt}

@orderBlueprint.route("/searchOrder/<int:page>/<int:cntPerPage>")
def search_Order(page,cntPerPage):
    '''

    :param page: 代表页数 从1开始 整数
    :param cntPerPage: 每一页有多少条数据 整数
    说明
        根据条件返回数据
        日期时间，经纬度范围（东北——西南），userid和bikeid
    可选参数
        bikeid
        userid
        NorthEast_location:{"x":,"y":} x除了两条116，其余全是121.xxx， y除了两条是40，其余全是31.xxx
        SouthWest_location:{"x":,"y":} x的取值范围在116~121左右， y的取值范围在30~40，和上面类似
            应保证 NorthEast_location.x>SouthWest_location.x  and NorthEast_location.y<SouthWest_location.y
        date_time：{"first":'2020-08-06 00:00:54',"second":'2020-08-07 17:53:53'}

    :return:
        return {"res":res}
    '''
    bikeid=request.args.get('bikeid')
    userid=request.args.get('userid')
    NorthEast_location = request.args.get('NorthEast_location')
    SouthWest_location=request.args.get('SouthWest_location')
    date_time=request.args.get('date_time')
    sql="select * from order_table where 1=1 "
    if(bikeid !=None):
        sql=sql+"and bikeid=%s "
    if(userid !=None):
        sql=sql+"and userid=%s "
    if(NorthEast_location!=None and SouthWest_location!=None):
        NorthEast_location = json.loads(NorthEast_location)
        SouthWest_location=json.loads(SouthWest_location)
        sql=sql+"and  start_location_x > %s and start_location_x <%s "
        sql=sql+"and  start_location_y > %s and start_location_y <%s "
    if(date_time!=None):
        date_time=json.loads(date_time)
        sql=sql+"and UNIX_TIMESTAMP(start_time) >%s and UNIX_TIMESTAMP(start_time) <%s "
    '''----------------------------------------------------------------------------------'''
    variable=[]
    if (bikeid != None):
        variable.append(bikeid)
    if (userid != None):
        variable.append(userid)
    if (NorthEast_location != None and SouthWest_location != None):
        variable.extend([SouthWest_location["x"],NorthEast_location["x"],NorthEast_location["y"],SouthWest_location["y"]])
    if (date_time != None):
        first_t=math.floor(datetime.datetime.strptime(date_time["first"],"%Y-%m-%d %H:%M:%S").timestamp())
        second_t = math.floor(datetime.datetime.strptime(date_time["second"],"%Y-%m-%d %H:%M:%S").timestamp())
        variable.extend([first_t,second_t])
    sql=sql + " limit %s,%s "
    variable.extend([(page-1)*cntPerPage,cntPerPage])
    res=query_sql(sql,tuple(variable))
    return {"res":res}


