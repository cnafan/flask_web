from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_openid import OpenID
from config import basedir


app=Flask(__name__)
app.config.from_object('config') #读取配置文件
db = SQLAlchemy(app)#创建了一个 db 对象（数据库）


lm = LoginManager()
lm.init_app(app)
oid = OpenID(app, os.path.join(basedir, 'tmp'))#一个存储文件的临时文件夹的路径
lm.login_view = 'login' #Flask-Login 需要知道哪个视图允许用户登录


from app import views, models,email
