from libs.orm import db
from user.models import Users


class Blogs(db.Model):
    __tablename__ = 'blog'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
    update_time = db.Column(db.DateTime, nullable=False)

    # 获取用户信息 blog.author
    @property
    # 将方法的结果变成类的一个属性
    def author(self):
        return Users.query.get(self.uid)


# 评论模型
class Comments(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, nullable=False, index=True)
    bid = db.Column(db.Integer, nullable=False, index=True)
    cid = db.Column(db.Integer, nullable=False, index=True, default=0)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)

    # 获取用户信息 comment.author
    @property
    # 将方法的结果变成类的一个属性
    def author(self):
        return Users.query.get(self.uid)

    @property
    def upper(self):
        '''上一级评论'''
        if self.cid == 0:
            return None
        else:
            return Comments.query.get(self.cid)
