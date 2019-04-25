
import redis
from flask import Flask,render_template
from flask_script import Manager
from flask_session import Session

from back.models import db
from back.views import back
from web.views import web

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

# 第三步: 注册蓝图,可以使用蓝图blue管理路由了
app.register_blueprint(blueprint=web,url_prefix='/web')
app.register_blueprint(blueprint=back,url_prefix='/back')
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1',port=6379)

# 加密方式
app.secret_key = 'fdtyd14124gytrwfh4t5765454u5643yufgrasfc'
Session(app)
# 配置数据库链接信息
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:234@127.0.0.1:3306/python1901'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

manage = Manager(app)

if __name__ == '__main__':
    manage.run()
