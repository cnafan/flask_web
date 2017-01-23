from app import app, db, lm, oid
from flask import render_template, flash, redirect, session, url_for, request, g
from .forms import LoginForm, EditForm,RegistrationForm
from .models import User
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Mail, Message
from datetime import datetime
import threading
from werkzeug.security import generate_password_hash,check_password_hash
#user_loader 回调，用于从数据库加载用户
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

#检查 g.user 为了决定用户是否已经登录
#任何使用了 before_request 装饰器的函数在接收请求之前都会运行
@app.before_request
def before_request():
    #在数据库中更新用户最后一次的访问时间
    g.user = current_user
    if g.user.is_authenticated:#去掉（），'bool' object is not callable
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()

@app.route('/')
@app.route('/index')
@login_required #添加了 login_required 装饰器，确保了这页只被已经登录的用户看到
def index():
    user =  g.user
    posts = [ # fake array of posts
        {
            'author': { 'nickname': 'John' },
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': { 'nickname': 'qiang' },
            'body': 'i love you!'
        }
    ]
    return render_template("index.html",
        title = 'Home',
        user = user,
        posts = posts)

@app.route('/confirm/<token>')
@login_required
def confirm(token):
    user =  g.user
    if user.confirmed:
        return redirect(url_for('index'))
    if user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return  redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=generate_password_hash(form.password.data),
                    phone=form.phone.data)
        db.session.add(user)
        db.session.commit()
        #token生成
        token = user.generate_confirmation_token()
        #sender 发送方哈，recipients 邮件接收方列表
        msg = Message("验证账户",sender='sikuquanshu123@163.com', recipients=['sikuquanshu12@163.com'])
        msg.html=render_template('confirm.html',user=user,token=token)
        mail = Mail(app)
        mail.send(msg)
        return redirect(url_for('login'))    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler #oid.loginhandle 告诉 Flask-OpenID 这是我们的登录视图函数
def login():
    
    form = LoginForm()
    #g 全局变量是一个在请求生命周期中用来存储和共享数据
    #g.user.is_authenticated()检查 g.user 是否被设置成一个认证用户
    if (g.user is not None) and g.user.is_authenticated:#去掉（），'bool' object is not callable
        #flash('已经登录')
        return redirect(url_for('index'))#是的话将会被重定向到首页
        #一个已经登录的用户的话，就不需要二次登录了 
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        #flash(str(form.email.data)+' 尝试登录.')
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))
        if not user.verify_password(form.password.data):
            flash('密码不正确.')
    return render_template('login.html',
                           title='登录',
                           form=form)
                           #,providers=app.config['OPENID_PROVIDERS'])
    
#resp 参数传入给 after_login 函数，它包含了从 OpenID 提供商返回来的信息
@oid.after_login
def after_login(resp):
    #flash('resp:'+str(resp))
    if resp.email is None or resp.email == "":
        flash('无效的登录，请重试.')
        return redirect(url_for('login'))
    #从数据库中搜索邮箱地址
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    flash('已退出当前账户.')
    return redirect(url_for('index'))

@app.route('/user')
#当客户端以 URL /user/miguel 请求的时候，视图函数收到一个nickname = ‘miguel’ 参数而被调用
@login_required
def user():
    username=g.user.username
    user = User.query.filter_by(username = username).first()
    if user == None:
        flash('User ' + username + ' not found.')
        return redirect(url_for('index'))
    posts = [
        { 'author': user, 'body': 'Test post #1' },
        { 'author': user, 'body': 'Test post #2' }
    ]
    return render_template('user.html',
        user = user,
        posts = posts)


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm()
    if form.validate_on_submit():
        g.user.username = form.username.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        return redirect(url_for('user'))
    else:
        form.username.data = g.user.username
        form.about_me.data = g.user.about_me
    return render_template('edit.html', form=form)

