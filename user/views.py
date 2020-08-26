from flask import Blueprint, request, redirect, session, render_template
import datetime

from user.models import Users
from libs.orm import db
from libs.utils import make_password, check_password, save_avatar, login_required
from sqlalchemy.orm.exc import NoResultFound

# 定义 blueprint 对象                    路由前缀
user_bp = Blueprint('user', __name__)
# 设置当前蓝图的模板⽂件夹位置
user_bp.template_folder = './templates'
# 设置当前蓝图的静态⽂件存放位置
user_bp.static_folder = './static'


# 通过 user_bp来绑定路由地址
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
            if password != password2:
                return render_template('register.html', error=1)
            else:
                u1 = Users(username=username, password=make_password(password),
                           tel=tel, birthday=birthday, gender=gender, created=now)

                if avatar:
                    u1.avatar = save_avatar(avatar)

                db.session.add(u1)
                db.session.commit()

            return redirect('/')


@user_bp.route('/', methods=("POST", "GET"))
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
            return redirect('/blog/')
        else:
            return render_template('login.html', error=2)


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

        return redirect('/')


@user_bp.route('/user/info')
@login_required
def info():
    uid = session.get('uid')
    user_info = Users.query.get(uid)
    return render_template('info.html', user_info=user_info)


@user_bp.route('/user/logout')
def logout():
    # 删除session数据
    session.clear()
    return redirect('/')
