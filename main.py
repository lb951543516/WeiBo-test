from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from user.views import user_bp
from blog.views import blog_bp
from libs.orm import db


# 定义对象
app = Flask(__name__)
# 配置SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:lb951543516@localhost:3306/weibo'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://lbsql:lb951543516@119.45.201.6:3306/lbbase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)

# 设置⼀个安全密钥
app.secret_key = r'qwrfsfasf784W34d5432e&*^%&@'

manager = Manager(app)

# 初始化数据库迁移工具
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

# 注册蓝图
app.register_blueprint(user_bp)
app.register_blueprint(blog_bp)


if __name__ == '__main__':
    manager.run()
