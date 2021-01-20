from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(UserMixin, db.Model):
    __tablename__ = 'systemreview_user_tb'  # 对应mysql数据库表
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, index=True)
    password = db.Column(db.String(20))
    phone=db.Column(db.String(20))
    email = db.Column(db.String(30))
    name = db.Column(db.String(30))
    organization = db.Column(db.String(200))

    # def __init__(self, username, password, email, name, organization):
    #     self.username = username
    #     self.password = password
    #     self.email = email
    #     self.name = name
    #     self.organization = organization

    # def __repr__(self):
    #     return '<User %s,%s,%s,%s,%s>' % self.username; % self.password
    #
    # def is_authenticated(self):
    #     return True
    #
    # def is_active(self):
    #     return True
    #
    # def is_anonymous(self):
    #     return False
