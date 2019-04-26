import math

from flask import Blueprint, request, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
# 第一步:生成蓝图对象
# 蓝图用于管理路由
from back.models import db, User, Article, ArticleType
from utils.functions import is_login

back = Blueprint('back', __name__)


# 第二步: 使用蓝图对象管理路由
@back.route('/')
def index1():
    return redirect(url_for('back.login'))


# index页面
@back.route('/index/', methods=['GET'])
@is_login
def index():
    if request.method == 'GET':
        return render_template('back/index.html', a='report',arts=request.arts,username=request.user, state=request.state, count=request.count)


# 注册操作
@back.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('back/register.html')
    if request.method == 'POST':
        # 获取数据
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        # print(username,password,password2)
        if username and password and password2:
            # 判断该账号是否被注册过
            user = User.query.filter(User.username == username).first()
            if user:
                # 判断该账号已注册,请更换账号
                error = '该账号已注册,请更换账号'
                return render_template('back/register.html', error=error)
            if password == password2:
                # 保存数据
                user = User()
                user.username = username
                user.password = generate_password_hash(password)
                # user.save_update()
                user.save_update()
                return redirect(url_for('back.login'))
            # 密码错误
            error = '两次密码不一致'
            return render_template('back/register.html', error=error)

        error = '请填写完整的信息'
        return render_template('back/register.html', error=error)


# 登陆操作
@back.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 模拟登陆
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            user = User.query.filter(User.username == username).first()
            if not user:
                error = '该账号不存在,请注册账号'
                return render_template('back/login.html', error=error)
            if not check_password_hash(user.password, password):
                error = '密码错误,请修改密码'
                return render_template('back/login.html', error=error)
            # 账号个密码匹配正确,跳转到首页
            session['user_id'] = user.id
            return redirect(url_for('back.index'))

        error = '请填写完整的信息'
        return render_template('back/login.html', error=error)
    return render_template('back/login.html')


# 退出操作
@back.route('/logout/', methods=['GET'])
@is_login
def logout():
    del session['user_id']
    return redirect(url_for('back.login'))


@back.route('/report/', methods=['GET'])
@is_login
def report():
    if request.method == 'GET':
        return render_template('back/report.html', a='report',arts=request.arts,username=request.user, state=request.state, count=request.count)



Number = 5
@back.route('/article/<int:page>/', methods=['GET'])
@is_login
def article1(page):
    if request.method == 'GET':
        pages = math.ceil(len(request.arts)/Number)
        art_list = Article.query.order_by(-Article.id).offset((page-1)*Number).limit(Number).all()
        return render_template('back/article.html', a='article', username=request.user, state=request.state,art_list=art_list,types=request.types,arts=request.arts,pages=pages,Number=Number)

@back.route('/article/', methods=['GET'])
@is_login
def article():
    if request.method == 'GET':
        pages = math.ceil(len(request.arts) / Number)
        art_list = Article.query.order_by(-Article.id).offset(0).limit(Number).all()
        return render_template('back/article.html', a='article', username=request.user, state=request.state, art_list=art_list, types=request.types,arts=request.arts,pages=pages,Number=Number)




@back.route('/add_article/', methods=['GET','POST'])
@is_login
def add_article():
    if request.method == 'GET':
        error =''
        return render_template('back/add_article.html', a='article', username=request.user, state=request.state,arts=request.arts,error=error,types=request.types)
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        type = request.form.get('category')
        print(title, content, type)
        if title:
            # 保存题目信息,判断该题目是否存在
            title_name = Article.query.filter(Article.title == title).first()
            if title_name:
                error = '该题目已有,请更换题目信息'
                return render_template('back/add_article.html', a='article', username=request.user, state=request.state ,types=request.types, error=error,content=content)
            articles = Article()
            articles.title = title
            articles.content = content
            articles.type = type
            # 添加数据到数据库
            db.session.add(articles)
            db.session.commit()
            return redirect(url_for('back.article'))

        else:
            error = '请填写题目信息'
            return render_template('back/add_article.html', a='article', username=request.user, state=request.state,error=error)


@back.route('/update_article/<int:id>/', methods=['GET','POST'])
@is_login
def update_article(id):
    if request.method == 'GET':
        art = Article.query.filter(Article.id == id).first()
        types = ArticleType.query.all()
        return render_template('back/update_article.html', a='article',id=id,art=art,types=types)
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        type = request.form.get('category')
        print(title,content,type)
        # art = Article.query.filter(Article.id == id).first()
        # types = ArticleType.query.all()
        # if title and type:
        #     # 保存栏目信息,判断该栏目是否存在
        #
        #     title_name = Article.query.filter(Article.title == title).first()
        #     type = Article.query.filter(Article.type == type).first()
        #
        #     if title_name and type:
        #         return redirect(url_for('back.article'))
        #     if title_name:
        #         # 判断该题目已有,请更换栏目信息
        #         error = '该题目已有,请更换栏目信息'
        #         return render_template('back/update_article.html',art=art, a='category',title_name = title_name,type = type,id=id,error=error,types=types)
        #     if type:
        #         # 判断该题目已有,请更换栏目信息
        #         error = '该题目已有,请更换栏目信息'
        #         return render_template('back/update_article.html', a='category',
        #                                title_name = title_name,art=art,type = type,id=id,error=error,types=types)
        articles = Article.query.filter(Article.id==id).first()
        articles.title = title
        articles.content = content
        articles.type = type
        # 添加数据到数据库
        db.session.add(articles)
        db.session.commit()
        return redirect(url_for('back.article'))


@back.route('/delete_article/<int:id>/', methods=['GET'])
@is_login
def delete_article(id):
    # 删除文章
    if request.method == 'GET':
        artid = Article.query.get(id)
        db.session.delete(artid)
        db.session.commit()
        return redirect(url_for('back.article'))

@back.route('/category/', methods=['GET','POST'])
@is_login
def category():
    if request.method == 'GET':
        return render_template('back/category.html', a='category', username=request.user, state=request.state,types=request.types)
    if request.method == 'POST':
        return render_template('back/category.html', a='category', username=request.user, state=request.state,types=request.types)


@back.route('/add_category/', methods=['GET', 'POST'])
@is_login
def add_category():
    if request.method == 'GET':
        return render_template('back/add_category.html', a='category', username=request.user, state=request.state)
    if request.method == 'POST':

        t_name = request.form.get('t_name')
        t_other_name = request.form.get('t_other_name')
        # print(t_name, t_other_name)
        if t_name and t_other_name:
            # 保存栏目信息,判断该栏目是否存在
            name = ArticleType.query.filter(ArticleType.t_name == t_name).first()
            other_name = ArticleType.query.filter(ArticleType.t_other_name == t_other_name).first()
            if name:
                # 判断该栏目已有,请更换栏目信息
                error = '该栏目已有,请更换栏目信息'
                return render_template('back/category.html', error=error,a='category', username=request.user, state=request.state,types=request.types)
            if other_name:
                # 判断该栏目已有,请更换栏目信息
                error = '该栏目别名已有,请更换栏目信息'
                return render_template('back/category.html', error=error,a='category', username=request.user, state=request.state,types=request.types)
            art_type = ArticleType()
            art_type.t_name = t_name
            art_type.t_other_name = t_other_name
            # 添加数据到数据库
            db.session.add(art_type)
            db.session.commit()
            return redirect(url_for('back.category'))

        else:
            error = '请填写栏目信息'
            return render_template('back/add_category.html', a='category', error=error, username=request.user,state=request.state)


@back.route('/update_category/<int:id>/', methods=['GET','POST'])
@is_login
def update_category(id):
    if request.method == 'GET':
        typeid = ArticleType.query.filter(ArticleType.id==id).first()
        t_name = typeid.t_name
        t_other_name = typeid.t_other_name
        return render_template('back/update_category.html', a='category',
                t_name = t_name,t_other_name = t_other_name,id=id)
    if request.method == 'POST':
        t_name = request.form.get('t_name')
        t_other_name = request.form.get('t_other_name')
        print(t_name, t_other_name)
        if t_name and t_other_name:
            # 保存栏目信息,判断该栏目是否存在
            name = ArticleType.query.filter(ArticleType.t_name == t_name).first()
            other_name = ArticleType.query.filter(ArticleType.t_other_name == t_other_name).first()

            if name and other_name:
                return redirect(url_for('back.category'))
            if name:
                # 判断该栏目已有,请更换栏目信息
                error = '该栏目已有,请更换栏目信息'
                return render_template('back/update_category.html', a='category',
                t_name = t_name,t_other_name = t_other_name,id=id,error=error)
            if other_name:
                # 判断该栏目别名已有,请更换栏目信息
                error = '该栏目别名已有,请更换栏目信息'
                return render_template('back/update_category.html', a='category',
                t_name = t_name,t_other_name = t_other_name,id=id,error=error)

            art_type = ArticleType.query.filter(ArticleType.id==id).first()
            art_type.t_name = t_name
            art_type.t_other_name = t_other_name
            # 添加数据到数据库
            db.session.add(art_type)
            db.session.commit()
            return redirect(url_for('back.category'))


@back.route('/delete_category/<int:id>/', methods=['GET'])
@is_login
def delete_category(id):
    # 删除分类
    if request.method == 'GET':
        typeid = ArticleType.query.get(id)
        for arts in typeid.arts:
            db.session.delete(arts)
        db.session.delete(typeid)
        db.session.commit()
        return redirect(url_for('back.category'))








































# 数据库操作

@back.route('/create_db/', methods=['GET'])
def create_db():
    # 生成数据库中的表
    # 将模型映射成数据库中的表(对第一次使用有用)
    db.create_all()
    return '创建表成功'


@back.route('/drop_db/', methods=['GET'])
def drop_db():
    # 删除数据库中所有的表
    db.drop_all()
    return '删除表成功'



