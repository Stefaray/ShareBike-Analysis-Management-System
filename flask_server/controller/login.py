from utils import *
from Global import *
from flask import request,session

'''
通过用户名和密码和验证码进行登陆 "/login"
'''
@loginBlueprint.route('/', methods=['POST'])
def login():
    '''
    参数列表
        username--用户名
        password--密码
        code---验证码
    说明
        请先使用 /login/code 获取验证码后，在使用此接口进行登陆
        请求参数的code值如果不等于 /login/code 返回值，将登陆失败
    :return:
        - 登陆成功
        - 验证码有误
        - 用户名或密码不正确
    '''
    
    username = request.form["username"]
    password = request.form["password"]
    code=request.form['code']
    res=query_sql("SELECT * FROM USER WHERE username=%s AND PASSWORD=%s and IDENTITY=%s",
              (username,password,1)) 
    # res=query_sql("SELECT * FROM USER WHERE username=%s AND PASSWORD=%s and IDENTITY=%s",
    #           (username,password,Identity.admin.value)) 
    
    # if(code!=session['code']):
    #     return '验证码有误'
    if(len(res)>0):
        session['user']=res[0]
        return '登陆成功'
    return '用户名或密码不正确'

@loginBlueprint.route('/login1', methods=['POST'])
def login1():
    return '1'

@loginBlueprint.route("/code", methods=['POST'])
def getcode():
    '''
    说明
        返回验证码
    参数：
        len【可选】
    返回值
        验证码【数字】
    '''
    # len = 3
    len=int(request.form["len"])
    if(len==None):
        len=4
    code=getRandomNum(len)
    session['code']=code
    return code

@loginBlueprint.route('/logout')
def logout():
    '''
   @@@
    #### 描述
        用户注销
    #### return
    - ##### string
    > 注销成功
    @@@
    '''
    session.pop('user',None)
    return '注销成功'



@userBlueprint.route('/getUser')
def get_User():
    '''
     说明
        得到当前用户
     返回值
        - 当前用户【json】
        - 当前没有用户登陆

     '''
    if(session.get('user')==None):
        return '当前没有用户登陆'
    return {"currentUser":session['user']}

