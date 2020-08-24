from flask import Blueprint, request, redirect, session
from flask import render_template

from blog.models import Blogs
from user.models import Users

from libs.orm import db
import datetime

blog_bp = Blueprint('blog', __name__, url_prefix='/blog')
blog_bp.template_folder = './templates'
blog_bp.static_folder = './static'


@blog_bp.route('/')
def home():
    uid = session.get('uid')
    user_info = Users.query.get(uid)

    blog = Blogs.query.order_by(Blogs.create_time.desc()).all()
    return render_template('home.html', user_info=user_info, blog=blog)


@blog_bp.route('/content')
def content():
    uid = session.get('uid')
    user_info = Users.query.get(uid)
    blog = Blogs.query.filter_by(author=user_info.username).order_by(Blogs.create_time.desc()).all()
    return render_template('content.html', blog=blog, user_info=user_info)


@blog_bp.route('/write', methods=("POST", "GET"))
def write():
    if request.method == "GET":
        uid = session.get('uid')
        user_info = Users.query.get(uid)
        return render_template('write.html', user_info=user_info)
    else:
        username = session.get('username')
        title = request.form.get('title')
        content = request.form.get('content')
        now = datetime.datetime.now()

        blog = Blogs(author=username, title=title, content=content, create_time=now)
        db.session.add(blog)
        db.session.commit()

        return redirect('/blog/read?id=%s' % blog.id)


@blog_bp.route('/read')
def read():
    uid = session.get('uid')
    user_info = Users.query.get(uid)
    bid = int(request.args.get('id'))
    blog = Blogs.query.get(bid)
    return render_template('read.html', blog=blog, bid=bid, user_info=user_info)


@blog_bp.route('/delete')
def delete():
    bid = int(request.args.get('id'))
    Blogs.query.filter_by(id=bid).delete()
    db.session.commit()
    return redirect('/blog/content')
