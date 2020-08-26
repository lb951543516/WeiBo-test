from flask import Blueprint, request, redirect, session
from flask import render_template
import datetime, math

from blog.models import Blogs
from user.models import Users
from libs.orm import db
from libs.utils import login_required

blog_bp = Blueprint('blog', __name__, url_prefix='/blog')
# blog_bp.template_folder = f'{base_dir}/blog/templates'
blog_bp.template_folder = './templates'
blog_bp.static_folder = './static'


@blog_bp.route('/')
def home():
    # 当前登录用户
    uid = session.get('uid')

    # 全部微博
    blog_num = Blogs.query.order_by(Blogs.update_time.desc()).count()

    # 分页
    page = int(request.args.get('page', 1))
    per_page = 6
    offset = per_page * (page - 1)
    max_pages = math.ceil(blog_num / per_page)

    if page <= 5:  # 开始页码范围
        if max_pages >= 10:
            start, end = 1, 10
        else:
            start, end = 1, max_pages
    elif page > max_pages - 5:  # 结束页码范围
        start, end = max_pages - 10, max_pages
    else:  # 中间页面范围
        start, end = page - 5, page + 5

    page_range = range(start, end + 1)
    blog = Blogs.query.order_by(Blogs.create_time.desc()).limit(per_page).offset(offset)

    return render_template('home.html', blog=blog, page_range=page_range, page=page, max_pages=max_pages)


# 个人微博内容
@blog_bp.route('/content')
@login_required
def content():
    uid = session.get('uid')
    # 全部微博
    blog_num = Blogs.query.filter_by(uid=uid).order_by(Blogs.update_time.desc()).count()

    # 分页
    page = int(request.args.get('page', 1))
    per_page = 6
    offset = per_page * (page - 1)
    max_pages = math.ceil(blog_num / per_page)

    if page <= 5:  # 开始页码范围
        if max_pages >= 10:
            start, end = 1, 10
        else:
            start, end = 1, max_pages
    elif page > max_pages - 5:  # 结束页码范围
        start, end = max_pages - 10, max_pages
    else:  # 中间页面范围
        start, end = page - 5, page + 5

    page_range = range(start, end + 1)
    blog = Blogs.query.filter_by(uid=uid).order_by(Blogs.update_time.desc()).limit(per_page).offset(offset)

    return render_template('content.html', blog=blog, page_range=page_range, page=page, max_pages=max_pages)


@blog_bp.route('/write', methods=("POST", "GET"))
@login_required
def write():
    if request.method == "GET":
        return render_template('write.html')
    else:
        uid = session.get('uid')
        content = request.form.get('content').strip()
        now = datetime.datetime.now()
        if not content:
            return render_template('write.html', error=1)

        blog = Blogs(uid=uid, content=content, create_time=now, update_time=now)
        db.session.add(blog)
        db.session.commit()

        return redirect('/blog/content')


@blog_bp.route('/read')
@login_required
def read():
    uid = session.get('uid')
    user_info = Users.query.get(uid)

    bid = int(request.args.get('id'))
    blog = Blogs.query.get(bid)

    return render_template('read.html', bid=bid, blog=blog, user_info=user_info)


@blog_bp.route('/delete')
@login_required
def delete():
    bid = int(request.args.get('id'))
    Blogs.query.filter_by(id=bid).delete()
    db.session.commit()
    return redirect('/blog/content')


@blog_bp.route('/update_wb', methods=("POST", "GET"))
@login_required
def update():
    if request.method == "GET":
        bid = int(request.args.get('id'))
        blog = Blogs.query.get(bid)
        return render_template('update_wb.html', blog=blog, bid=bid)
    else:
        bid = int(request.form.get('bid'))
        content = request.form.get('content').strip()
        now = datetime.datetime.now()

        if not content:
            return render_template('update_wb.html', error=1)

        Blogs.query.filter_by(id=bid).update({'content': content, 'update_time': now})
        db.session.commit()
        return redirect('/blog/content')
