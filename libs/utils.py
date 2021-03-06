import os
from functools import wraps
from hashlib import sha256, md5
from urllib.parse import quote

from flask import session,redirect,request


def make_password(password):
    '''加密'''
    if not isinstance(password, bytes):
        password = str(password).encode('utf8')

    # 计算哈希值
    hash_value = sha256(password).hexdigest()

    # 加盐
    salt = os.urandom(16).hex()

    # 产生安全密码
    new_password = salt + hash_value

    return new_password


def check_password(password, new_password):
    '''检查密码'''
    if not isinstance(password, bytes):
        password = str(password).encode('utf8')

    # 计算哈希值
    hash_value = sha256(password).hexdigest()

    return hash_value == new_password[32:]


def save_avatar(avatar_file):
    '''保存头像文件'''
    # 读取文件的二进制数据
    file_bin_data = avatar_file.stream.read()

    # 文件指针归零
    avatar_file.stream.seek(0)

    # 计算文件的 md5 值
    filename = md5(file_bin_data).hexdigest()

    # 获取项目文件夹的绝对路径
    # os.path.abspath(__file__)  utils的绝对路径
    # os.path.dirname(os.path.abspath(__file__)) libs的绝对路径
    # os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 项目的绝对路径
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # 文件绝对路径
    filepath = os.path.join(base_dir, 'static', 'upload', filename)

    # 保存文件
    avatar_file.save(filepath)

    # 文件的 URL
    avatar_url = f'/static/upload/{filename}'

    return avatar_url


def login_required(view_func):
    @wraps(view_func)
    # 函数被装饰器装饰后 会变成装饰器的内部函数
    # wraps可以防止发生这种情况，让被装饰的函数保持其本身
    def check_session(*args, **kwargs):
        uid = session.get('uid')
        if not uid:
            # from_url=quote(request.full_path)
            return redirect('/user/login')
        else:
            return view_func(*args, **kwargs)

    return check_session
