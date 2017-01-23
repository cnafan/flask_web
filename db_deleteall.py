from app import db, models

#数据库清空
users = models.User.query.all()
for u in users:
    db.session.delete(u)
posts = models.Post.query.all()
for p in posts:
    db.session.delete(p)
db.session.commit()
print("已清空")
