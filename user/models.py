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
