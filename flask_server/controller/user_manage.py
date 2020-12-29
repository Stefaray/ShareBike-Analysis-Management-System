from utils import *
from Global import *
from flask import request,session

import datetime
import time
import math
import json
import pytz
from datetime import datetime,timedelta


@userBlueprint.route("/addUser",methods=['POST'])
def add_User():
    '''
    说明
        添加用户
    参数
        - username用户名
        - password密码
        - identity身份 【管理员是0，其他是1】
        - phone手机号【可选】
        - email 邮箱【可选】
        - money 余额【可选】
    :return:
        - {msg:添加用户成功,user:[json]}
        - 用户名已存在
        - 金额输入有误
    '''
    username=request.form["username"]
    password=request.form["password"]
    identity=request.form["identity"]
    phone=genPhone() if request.form.get("phone")==None else request.form["phone"]
    email =genEmail()  if request.form.get("email") == None else request.form["email"]
    money =99  if request.form.get("money") == None else request.form["money"]
    try:
        money=int(money)
        if(money<0):
            return '金额输入有误'
    except:
        return '金额输入有误'

    maxid=query_sql("select max(userid) from user")[0]['max(userid)']
    # print(maxid)
    userid=maxid+1
    cnt=update_sql("insert ignore into user(userid,register_date,username,password,identity,phone,email,money) "
               "values(%s,%s,%s,%s,%s,%s,%s,%s)",(userid,datetime.now(),username,password,identity,phone,email
                                               ,money))
    if(cnt==1):
        user=query_sql("select * from user where userid=%s",(userid))
        return {"msg":'添加用户成功',"user":user}
    return '用户名已存在'

@userBlueprint.route("/delUser")
def del_User():
    '''
    说明
        通过用户名或userid 来删除一个用户,如果一个都没有，则无法删除
    参数
        userid【可选】
        username【可选】
    :return:
        - 请至少输入userid和username中的一个参数
        - 删除成功
        - 没有该用户
    '''
    userid=request.args.get("userid",None)

    username=request.args.get("username",None)

    cnt=0
    if(username!=None):

        cnt=update_sql("delete from user where username=%s",(username))
    elif(userid!=None):

        cnt=update_sql("delete from user where userid = %s",(userid))
    else:
        return '请至少输入userid和username中的一个参数'

    if(cnt>0):
        return '删除成功'
    return '没有该用户'

@userBlueprint.route("/userInfo")
def get_User_Info():
    '''
    说明
        获得用户详细信息
    参数列表
        username 用户名
    :return:
        - {"info":[json]}
        - 没有该用户
    '''
    username=request.args.get("username")
    res=query_sql("select * from user where username=%s",(username))[0]
    if(len(res)==0):
        return '没有该用户'
    return {"info":res}


@userBlueprint.route("/rideHistory")
def ride_History():
    '''
    说明
        返回最近days天的骑行历史，days可以不指定

    参数
        userid
        days[可选] 如果不指定，返回用户所有的历史，如果指定，返回从今天起前days天的骑行历史
    返回
        -用户最近骑行总次数
        -最近骑行总公里数
        -用户最近骑行历史列表：遍历每一次骑行记录
            - 骑行起点和终点
            - 骑行起时间
            - 骑行终止时间
            - 骑行路程
            - 骑行车辆编号
            - 骑行轨迹
    '''
    userid = request.args.get("userid")
    days=request.args.get("days")
    if(days==None):
        res = query_sql("SELECT * FROM order_table WHERE userid=%s",(userid))

    else:
        date=datetime.now()+timedelta(days=-days)
        res=query_sql("SELECT * FROM order_table WHERE userid=%s and start_time > %s",(userid,date))
    totalDis=0
    L=[]
    for ride in res:
        print(ride)
        x1=ride["start_location_x"]
        y1=ride["start_location_y"]
        x2=ride["end_location_x"]
        y2=ride["end_location_y"]
        dis=haversine(x1,y1,x2,y2)
        ride["distance"]=dis
        totalDis+=dis
        L.append(ride)

    return {"history": L,"count":len(L),"totalDistance":totalDis}

@userBlueprint.route("/updateUser",methods=['POST'])
def update_User():
    '''
    说明
        更新用户信息
    参数
        username 用户名
        - 可选参数
            password
            phone
            email
            money
            identity
    :return:
        - 用户名有误
        - {"msg":xxx更新完成,"user":[json]}
    '''
    username=request.form.get("username")
    password=request.form.get("password")
    phone=request.form.get("phone")
    email=request.form.get("email")
    money=request.form.get("money")
    identity=request.form.get("identity")
    res=query_sql("select * from user where username=%s",(username))
    if(len(res)==0):
        return '用户名有误'
    ans=""
    if(password!=None):
        cnt=update_sql("UPDATE  USER SET PASSWORD=%s WHERE username=%s",(password,username))

        if(cnt==0):
            ans+='密码未更新\n'
        else:
            ans += '密码更新完成\n'
    if (phone != None):
        cnt = update_sql("UPDATE  USER SET phone=%s WHERE username=%s", (phone, username))

        if(cnt==0):
            ans+='手机号未更新\n'
        else:
            ans += '手机号更新完成\n'
    if(email!=None):
        cnt=update_sql("UPDATE  USER SET email=%s WHERE username=%s",(email,username))

        if(cnt==0):
            ans+='邮箱未更新\n'
        else:
            ans += '邮箱更新完成\n'
    if(money!=None):
        cnt=update_sql("UPDATE  USER SET money=%s WHERE username=%s",(money,username))

        if(cnt==0):
            ans+='余额未更新\n'
        else:
            ans += '余额更新完成\n'
    if(identity!=None):
        cnt=update_sql("UPDATE  USER SET identity=%s WHERE username=%s",(identity,username))

        if(cnt==0):
            ans+='身份未更新\n'
        else:
            ans += '身份更新完成\n'
    user = query_sql("select * from user where username=%s", (username))[0]
    return {'msg':ans,"user":user}






# 显示所有订单列表
@userBlueprint.route("/order_table", methods=['POST'])
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
    if(importance == '用户ID'):
        importance = 'userid'
    elif(importance == '用户名'):
        importance = 'username'
    elif(importance == '注册时间'):
        importance = 'register_date'
    elif(importance == '电话'):
        importance = 'phone'
    elif(importance == '邮箱'):
        importance = 'email'
    elif(importance == '余额'):
        importance = 'money'
    elif(importance == '用户类别'):
        importance = 'identity'
    
    

    if(title != ''):
        print(importance)
        print(title)
        print(str(least_piece) +'-------------------')
        # cursor.execute('Select * From user Where '+ importance +' like \'%'+title+'%\' limit ' + str(least_piece) + ', ' + str(limit) )
        result = query_sql('Select * From user Where '+ importance +' like \'%'+title+'%\' limit ' + str(least_piece) + ', ' + str(limit))
        # print(result)
        total = query_sql('Select count(*) as num From user Where '+ importance +' like \'%'+title+'%\'')

    else:
        result = query_sql('Select * From user LIMIT ' + str(least_piece) + ', ' + str(limit) )
        # result = cursor.fetchall()
        total = query_sql('Select count(*) as num From user')
        # total = cursor.fetchall()
    
    total = total[0]["num"]
    returnmsg={"code":20000,"desc":"UID接收成功","items":result,"total":total}


    return returnmsg


# 增加订单
@userBlueprint.route("/order_ADD",methods=["POST"])
def order_ADD():
    returnmsg = []
    params = request.form["data"]
    print(params)
    
    param = json.loads(params)
    # userid = str(param["userid"])
    username = str(param["username"])
    password = str(param["password"])
    # register_date = str(param["register_date"])
    phone = str(param["phone"])
    email = str(param["email"])
    money  = str(param["money"])
    identity = str(1)
    userid = int(time.time())
    userid = str(userid)
    print( '---------------------------------------')

    update_sql("insert user(userid,register_date,username,phone,email,money,password,identity) values(%s,%s,%s,%s,%s,%s,%s,%s)",(userid,datetime.now(),username,phone,email,money,password,identity))


    returnmsg={"code":20000,"desc":"UID接收成功","userid":userid}
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
@userBlueprint.route("/order_UPDATE",methods=["POST"])
def order_UPDATE():
    returnmsg = []
    params = request.form["data"]
    print(params)
    
    param = json.loads(params)
    userid = str(param["userid"])
    username = str(param["username"])
    password = str(param["password"])
    phone = str(param["phone"])
    email = str(param["email"])
    money = str(param["money"])

    print(money)
    # cursor.execute('Update order_table Set bikeid="'+bikeid+'",userid='+userid+' where orderid = ' + orderid ) 
    update_sql('Update user Set identity='+'1'+',username='+username+',password='+password+',phone='+phone+',email='+email+',money='+money+ ' Where userid = ' + userid) 


    returnmsg={"code":20000,"desc":"UID接收成功","userid":1}
    return returnmsg


# 删除订单
@userBlueprint.route("/order_DELETE",methods=["POST"])
def order_DELETE():
    returnmsg = []
    params = request.form["data"]
    print(params)
    param = json.loads(params)
    userid = str(param["userid"])


    # print( '---------------------------------------')

    update_sql('Delete From user Where userid = ' + userid ) 

    

    returnmsg={"code":20000,"desc":"UID接收成功","userid":1}
    return returnmsg

# 删除订单
@userBlueprint.route("/user_SWITCH",methods=["POST"])
def user_SWITCH():
    returnmsg = []
    params = request.form["data"]
    print(params)
    param = json.loads(params)
    userid = str(param["userid"])
    identity = str(param["identity"])
    print(param)
    print(identity)
    if(identity == '0'):
        switch_identity = '1'
    else:
        switch_identity = '0'
    # print( '---------------------------------------')

    update_sql('Update user Set identity = '+switch_identity+' Where userid = ' + userid ) 

    

    returnmsg={"code":20000,"desc":"UID接收成功","userid":1}
    return returnmsg




