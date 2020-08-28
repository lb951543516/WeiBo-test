from libs.orm import db


# 定义表结构
class Users(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    tel = db.Column(db.String(20), nullable=False)
    birthday = db.Column(db.Date, default='1960-01-01')
    gender = db.Column(db.Enum('male', 'female'))
    avatar = db.Column(db.String(256), default='/static/img/default.jpg')
    created = db.Column(db.DateTime, nullable=False)
    n_follow=db.Column(db.Integer,nullable=False,default=0)
    n_fan=db.Column(db.Integer,nullable=False,default=0)


# 关注表结构
class Follows(db.Model):
    __tablename__ = 'follow'

    uid = db.Column(db.Integer, primary_key=True)
    fid = db.Column(db.Integer, primary_key=True)
