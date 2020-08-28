from flask import Blueprint
from flask import request
from flask import redirect
from flask import render_template
from flask import session
import datetime

from urllib.parse import unquote
from user.models import Users
from user.models import Follows
from blog.models import Blogs

from libs.orm import db
from libs.utils import make_password
from libs.utils import check_password
from libs.utils import save_avatar
from libs.utils import login_required

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError

# 定义 blueprint 对象                    路由前缀
user_bp = Blueprint('user', __name__)
# 设置当前蓝图的模板⽂件夹位置
user_bp.template_folder = './templates'
# 设置当前蓝图的静态⽂件存放位置
user_bp.static_folder = './static'


# 通过 user_bp来绑定路由地址
# 注册
@user_bp.route('/user/register', methods=("POST", "GET"))
def register():
    if request.method == "GET":
        return render_template('register.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        tel = request.form.get('tel')
        birthday = request.form.get('birthday')
        gender = request.form.get('gender')
        now = datetime.datetime.now()
        avatar = request.files.get('avatar')

        try:
            Users.query.filter_by(username=username).one()
            return render_template('register.html', error=2)
        except NoResultFound:
            if not password or password != password2:
                return render_template('register.html', error=1)
            else:
                u1 = Users(username=username, password=make_password(password),
                           tel=tel, birthday=birthday, gender=gender, created=now)

                if avatar:
                    u1.avatar = save_avatar(avatar)

                db.session.add(u1)
                db.session.commit()

            return redirect('/user/login')


# 欢迎页面
@user_bp.route('/')
def welcome():
    return render_template('welcome.html')


# 登录
@user_bp.route('/user/login', methods=("POST", "GET"))
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            u1 = Users.query.filter_by(username=username).one()
        except NoResultFound:
            return render_template('login.html', error=1)

        if check_password(password, u1.password) is True:
            session['uid'] = u1.id
            session['username'] = u1.username

            return redirect('/blog')
        else:
            return render_template('login.html', error=2)


# 修改个人信息
@user_bp.route('/user/update', methods=("POST", "GET"))
def update():
    uid = session.get('uid')
    user_info = Users.query.get(uid)

    if request.method == "GET":
        return render_template('update.html', user_info=user_info)
    else:
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        new_tel = request.form.get('tel')

        if check_password(old_password, user_info.password) is False:
            return render_template('update.html', error=1, user_info=user_info)
        else:
            user_info.password = make_password(new_password)
            user_info.tel = new_tel
            db.session.commit()
            session.clear()
        return redirect('/')


# 查看用户信息
@user_bp.route('/user/info')
@login_required
def info():
    blog_uid = int(request.args.get('uid'))
    user_info = Users.query.get(blog_uid)

    return render_template('info.html', user_info=user_info)


# 查看其他用户信息
@user_bp.route('/user/other_info')
@login_required
def other_info():
    uid = session.get('uid')

    # 微博信息
    bid = int(request.args.get('bid'))

    # 微博作者信息
    blog_author_id = int(request.args.get('uid'))
    user_info = Users.query.get(blog_author_id)

    # 判断是否关注过
    follow_num = Follows.query.filter_by(uid=uid, fid=blog_author_id).count()
    if follow_num == 0:
        is_follow = 0
    else:
        is_follow = 1

    return render_template('other_info.html', is_follow=is_follow, user_info=user_info, bid=bid)


# 退出
@user_bp.route('/user/logout')
def logout():
    # 删除session数据
    session.clear()
    return redirect('/')


# 关注他人
@user_bp.route('/user/follow')
@login_required
def follow():
    # pig 决定跳转到那一页
    pid = int(request.args.get('pid'))

    bid = int(request.args.get('bid'))
    fid = int(request.args.get('fid'))
    uid = session.get('uid')

    follow = Follows(uid=uid, fid=fid)

    try:
        # 关注
        Users.query.filter_by(id=uid).update({'n_follow': Users.n_follow + 1})
        Users.query.filter_by(id=fid).update({'n_fan': Users.n_fan + 1})
        db.session.add(follow)
        db.session.commit()
    except IntegrityError:
        # 取消点赞
        db.session.rollback()
        Users.query.filter_by(id=uid).update({'n_follow': Users.n_follow - 1})
        Users.query.filter_by(id=fid).update({'n_fan': Users.n_fan - 1})
        Follows.query.filter_by(uid=uid, fid=fid).delete()
        db.session.commit()

    if pid == 1:
        return redirect(f'/user/other_info?uid={fid}&bid={bid}')
    elif pid == 0:
        return redirect(f'/blog/read?bid={bid}')


# 查看粉丝列表
@user_bp.route('/user/your_fans')
@login_required
def show_fans():
    uid = session.get('uid')
    fans = Follows.query.filter_by(fid=uid).values('uid')
    fans_uid_list = [uid for (uid,) in fans]

    fans_info = Users.query.filter(Users.id.in_(fans_uid_list))
    return render_template('your_fans.html', fans_info=fans_info)


# 查看关注的人
@user_bp.route('/user/your_follows')
@login_required
def show_follows():
    uid = session.get('uid')
    follows = Follows.query.filter_by(uid=uid).values('fid')
    follows_fid_list = [fid for (fid,) in follows]

    follows_info = Users.query.filter(Users.id.in_(follows_fid_list))
    return render_template('your_follows.html', follows_info=follows_info)
