from libs.orm import db
from user.models import Users


class Blogs(db.Model):
    __tablename__ = 'blog'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
    update_time = db.Column(db.DateTime, nullable=False)

    @property
    def author(self):
        return Users.query.get(self.uid)