import os
from hashlib import sha256


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
