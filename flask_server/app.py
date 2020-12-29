from flask import Flask
from flask_docs import ApiDoc
from controller.login import *
from Global import *
import controller.user_manage
import controller.DataVisulization
import controller.order_manage
from flask_cors import CORS

app = Flask(__name__)
cors=CORS(app, supports_credentials=True, resources=r'/*')

'''配置session加密'''
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config['SESSION_USE_SIGNER'] = True


'''自动生成api文档'''
app.config['API_DOC_MEMBER'] = ['login','user','data','order']
# 需要排除的 RESTful Api 文档
app.config['RESTFUL_API_DOC_EXCLUDE'] = []
ApiDoc(app,title='共享单车接口文档')
app.register_blueprint(userBlueprint)
app.register_blueprint(loginBlueprint)
app.register_blueprint(orderBlueprint)
app.register_blueprint(dataBlueprint)



@app.route('/')
def hello_world():
    return 'Hello World!!'


if __name__ == '__main__':
    app.run(debug=True)
