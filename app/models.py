from app import db
from app import app
from werkzeug.security import generate_password_hash,check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

#添加了一个 Post 类，这是用来表示用户编写的 blog，在 Post 类中的 user_id 字段初始化成外键，因此 Flask-SQLAlchemy 知道这个字段是连接到用户上。
class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = False)
    password=db.Column(db.String(12), index=False, unique=False)
    email = db.Column(db.String(120), unique = True)
    phone=db.Column(db.String(12), index=False, unique=True)
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')
    confirmed = db.Column(db.Boolean, default=False)
    #增加两个字段：用户访问页面的最后一次的时间，自我介绍
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
  
    def is_authenticated(self):
        return True
    def verify_password(self,string):
        return check_password_hash(self.password, string)
        
    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})
    
    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % (self.nickname)
    #generate_confirmation_token()方法初始了一个包含默认失效时间的token，confirm() 方法会校验token的合法性并设置新增加的属性confirmed的值。
 
    #confirm() 方法除了校验token的值，还对校验得出的数据中的id和已经登录用户的id进行比对，这就确保了一点：就算你能够format一个正确的token，你仍旧没法保证该token跟已经登录的用户是匹配的。
    def confirm(self, token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True
