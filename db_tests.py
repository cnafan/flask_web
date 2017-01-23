from app import db, models
"""
u = models.User(nickname='john', email='john@email.com')
db.session.add(u)
db.session.commit()

#db.session.rollback() 可以是数据库回到会话开始的状态，如果即没有 commit 也没有 rollback 发生，系统默认情况下会回滚会话
"""
u = models.User(username='qiang', email='1@1.com',password='1')
db.session.add(u)
db.session.commit()

"""
#查询用户
users = models.User.query.all()
print users
#[<User u'john'>, <User u'susan'>]
for u in users:
    print u.id,u.nickname
#查询用户2
u = models.User.query.get(1)

import datetime
u = models.User.query.get(1)
p = models.Post(body='my first post!', timestamp=datetime.datetime.utcnow(), author=u)
#在 author 字段上存储了一个 User 对象
db.session.add(p)
db.session.commit()

u = models.User.query.get(1)
print(u)
posts = u.posts.all()
print(posts)

#get all users in reverse alphabetical order
print (models.User.query.order_by('nickname desc').all())

"""
