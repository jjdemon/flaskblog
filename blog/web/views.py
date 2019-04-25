
from flask import Blueprint, request,render_template,redirect,url_for

# 避免循环引入,删除没用的导包
# from manage import app

# 第一步:生成蓝图对象
# 蓝图用于管理路由
web = Blueprint('web',__name__)

# 第二步: 使用蓝图对象管理路由
@web.route('/')
def index():
    return render_template('web/index.html')
# @blue.route('/index/')
# def index1():
#     return redirect(url_for('first.index'))

@web.route('/about/',methods=['GET'])
def about():
    if request.method == 'GET':
        return render_template('web/about.html')

@web.route('/gbook/',methods=['GET'])
def gbook():
    if request.method == 'GET':
        return render_template('web/gbook.html')

@web.route('/index/',methods=['GET'])
def index1():
    if request.method == 'GET':
        return render_template('web/index.html')

@web.route('/info/',methods=['GET'])
def info():
    if request.method == 'GET':
        return render_template('web/info.html')

@web.route('/infopic/',methods=['GET'])
def infopic():
    if request.method == 'GET':
        return render_template('web/infopic.html')

@web.route('/list/',methods=['GET'])
def list():
    if request.method == 'GET':
        return render_template('web/list.html')

@web.route('/share/',methods=['GET'])
def share():
    if request.method == 'GET':
        return render_template('web/share.html')