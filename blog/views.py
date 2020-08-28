from flask import Blueprint
from flask import request
from flask import session
from flask import redirect
from flask import render_template
import datetime
import math

from blog.models import Blogs
from blog.models import Comments
from blog.models import Thumbs
from user.models import Follows

from libs.orm import db
from libs.utils import login_required

from sqlalchemy.exc import IntegrityError

# 定义蓝图
blog_bp = Blueprint('blog', __name__, url_prefix='/blog')
# blog_bp.template_folder = f'{base_dir}/blog/templates'
blog_bp.template_folder = './templates'
blog_bp.static_folder = './static'


# 微博首页
@blog_bp.route('/')
def home():
    # ---------------------- 分页
    blog_num = Blogs.query.order_by(Blogs.update_time.desc()).count()

    page = int(request.args.get('page', 1))
    per_page = 6  # 每页显示6个内容
    offset = per_page * (page - 1)
    max_pages = math.ceil(blog_num / per_page)  # 总页数

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


# 发布微博
@blog_bp.route('/write', methods=("POST", "GET"))
@login_required
def write():
    if request.method == "GET":
        return render_template('write.html')
    else:
        uid = session.get('uid')
        content1 = request.form.get('content', '').strip()
        now = datetime.datetime.now()
        if not content1:
            return render_template('write.html', error=1)

        blog = Blogs(uid=uid, content=content1, create_time=now, update_time=now)
        db.session.add(blog)
        db.session.commit()

        return redirect('/blog/content')


# 查看微博内容
@blog_bp.route('/read')
@login_required
def read():
    uid = session.get('uid')
    bid = int(request.args.get('bid'))
    blog = Blogs.query.get(bid)

    comment = Comments.query.filter_by(bid=bid).order_by(Comments.create_time.desc())

    # 判断是否点过赞
    thumb_num = Thumbs.query.filter_by(uid=uid, bid=bid).count()
    if thumb_num == 0:
        is_thumb = 0
    else:
        is_thumb = 1

    # 判断是否关注过
    follow_num = Follows.query.filter_by(uid=uid, fid=blog.author.id).count()
    if follow_num == 0:
        is_follow = 0
    else:
        is_follow = 1

    return render_template('read.html', blog=blog, comment=comment, is_thumb=is_thumb,is_follow=is_follow)


# 删除微博
@blog_bp.route('/delete')
@login_required
def delete():
    bid = int(request.args.get('bid'))
    Blogs.query.filter_by(id=bid).delete()
    db.session.commit()
    return redirect('/blog/content')


# 修改微博
@blog_bp.route('/update_wb', methods=("POST", "GET"))
@login_required
def update():
    if request.method == "GET":
        bid = int(request.args.get('bid'))
        blog = Blogs.query.get(bid)
        return render_template('update_wb.html', blog=blog)
    else:
        bid = int(request.form.get('bid'))
        blog=Blogs.query.get(bid)
        content = request.form.get('content', '').strip()
        now = datetime.datetime.now()

        if not content:
            return render_template('update_wb.html', error=1,blog=blog)

        Blogs.query.filter_by(id=bid).update({'content': content, 'update_time': now})
        db.session.commit()
        return redirect('/blog/content')


# 评论微博
@blog_bp.route('/write_comment', methods=("POST",))
@login_required
def write_comment():
    '''写评论'''
    uid = session.get('uid')
    bid = int(request.form.get('bid'))
    content = request.form.get('comment', '').strip()
    now = datetime.datetime.now()

    # 如果评论是空
    if not content:
        bid = int(request.form.get('bid'))
        blog = Blogs.query.get(bid)
        comment = Comments.query.filter_by(bid=bid).order_by(Comments.create_time.desc())
        return render_template('read.html', error=1, blog=blog, comment=comment)

    comment = Comments(uid=uid, bid=bid, content=content, create_time=now)
    db.session.add(comment)
    db.session.commit()
    return redirect(f'/blog/read?bid={bid}')


# 回复评论
@blog_bp.route('/reply_comment', methods=("POST",))
@login_required
def reply_comment():
    bid = int(request.form.get('bid'))
    cid = int(request.form.get('cid'))
    content = request.form.get('content', '').strip()
    uid = session.get('uid')
    now = datetime.datetime.now()

    # 如果回复是空
    if not content:
        bid = int(request.form.get('bid'))
        blog = Blogs.query.get(bid)
        comment = Comments.query.filter_by(bid=bid).order_by(Comments.create_time.desc())
        return render_template('read.html', error=2, blog=blog, comment=comment)

    comment = Comments(uid=uid, bid=bid, cid=cid, content=content, create_time=now)
    db.session.add(comment)
    db.session.commit()
    return redirect(f'/blog/read?bid={bid}')


# 删除评论
@blog_bp.route('/delete_comment')
@login_required
def delete_comment():
    comment_id = int(request.args.get('comment_id'))
    cmt = Comments.query.get(comment_id)

    # 修改数据
    cmt.content = '当前评论已被删除'
    db.session.commit()
    return redirect(f'/blog/read?bid={cmt.bid}')


# 点赞
@blog_bp.route('/thumb')
@login_required
def thumb():
    bid = int(request.args.get('bid'))
    uid = session.get('uid')

    thumb = Thumbs(uid=uid, bid=bid)
    try:
        # 点赞
        Blogs.query.filter_by(id=bid).update({'n_thumb': Blogs.n_thumb + 1})
        db.session.add(thumb)
        db.session.commit()
    except IntegrityError:
        # 取消点赞
        db.session.rollback()
        Blogs.query.filter_by(id=bid).update({'n_thumb': Blogs.n_thumb - 1})
        Thumbs.query.filter_by(uid=uid, bid=bid).delete()
        db.session.commit()

    return redirect(f'/blog/read?bid={bid}')
