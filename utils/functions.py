from functools import wraps

from flask import session,redirect,url_for, request

from back.models import User, ArticleType, Article


def is_login(func):
    @wraps(func)
    def check(*args, **kwargs):
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        # print(user.username)

        if user_id:
            request.user = user.username
            request.count = len(User.query.filter().all())
            request.state = '退出登录'
            request.types = ArticleType.query.all()
            request.arts = Article.query.all()
            return func(*args, **kwargs)
        else:
            return redirect(url_for('back.login'))
    return check