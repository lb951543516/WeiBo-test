from flask import Blueprint, request, redirect, session
from flask import render_template
import datetime

from blog.models import Blogs
from user.models import Users
from libs.orm import db

blog_bp = Blueprint('blog', __name__, url_prefix='/blog')
# blog_bp.template_folder = f'{base_dir}/blog/templates'
blog_bp.template_folder = './templates'
blog_bp.static_folder = './static'


@blog_bp.route('/')
def home():
    uid = session.get('uid')
    user_info = Users.query.get(uid)
    blog = Blogs.query.order_by(Blogs.create_time.desc()).all()

    return render_template('home.html', blog=blog, user_info=user_info)


@blog_bp.route('/content')
def content():
    uid = session.get('uid')

    blog = Blogs.query.filter_by(uid=uid).order_by(Blogs.create_time.desc()).all()
    return render_template('content.html', blog=blog)


@blog_bp.route('/write', methods=("POST", "GET"))
def write():
    if request.method == "GET":
        return render_template('write.html')
    else:
        uid = session.get('uid')
        content = request.form.get('content')
        now = datetime.datetime.now()
        if not content:
            return render_template('write.html', error=1)

        blog = Blogs(uid=uid, content=content, create_time=now, update_time=now)
        db.session.add(blog)
        db.session.commit()

        return redirect('/blog/content')


@blog_bp.route('/read')
def read():
    uid = session.get('uid')
    user_info = Users.query.get(uid)

    bid = int(request.args.get('id'))
    blog = Blogs.query.get(bid)

    return render_template('read.html', bid=bid, blog=blog, user_info=user_info)


@blog_bp.route('/delete')
def delete():
    bid = int(request.args.get('id'))
    Blogs.query.filter_by(id=bid).delete()
    db.session.commit()
    return redirect('/blog/content')


@blog_bp.route('/update_wb', methods=("POST", "GET"))
def update():
    if request.method == "GET":
        bid = int(request.args.get('id'))
        blog = Blogs.query.get(bid)
        return render_template('update_wb.html', blog=blog, bid=bid)
    else:
        bid = int(request.form.get('bid'))
        content = request.form.get('content')
        now = datetime.datetime.now()

        if not content:
            return render_template('update_wb.html', error=1)

        Blogs.query.filter_by(id=bid).update({'content': content, 'update_time': now})
        db.session.commit()
        return redirect('/blog/content')
