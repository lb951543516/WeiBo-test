from libs.orm import db


class Blogs(db.Model):
    __tablename__ = 'blog'

    id = db.Column(db.Integer, primary_key=True)
    author=db.Column(db.String(20),nullable=False)
    title = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime)
