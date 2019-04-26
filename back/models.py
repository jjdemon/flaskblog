from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()





class User(db.Model):
    # 定义自增的主键id字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 定义可变长度为10,且唯一的那么字段
    username = db.Column(db.String(255), unique=True, nullable=False)
    # 定义可变长度为255,且不设置唯一的那么字段
    password = db.Column(db.String(255), nullable=False)
    id_dalete = db.Column(db.Boolean, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)

    # 关联数据库中表名为user的表
    # __tablename__不写,则表示模型对应的表名称为模型名的小写
    __tablename__ = 'user'


    def save_update(self):
        db.session.add(self)  # 可写可不写
        db.session.commit()


    def delete(self):
        db.session.delete(self)
        db.session.commit()

class ArticleType(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    t_name = db.Column(db.String(255), unique=True, nullable=False)
    t_other_name = db.Column(db.String(255), unique=True, nullable=False)
    arts = db.relationship('Article',backref='tp')

    __tablename__ = 'art_type'


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    type = db.Column(db.Integer,db.ForeignKey('art_type.id'))