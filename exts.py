'''
该文件是为了避免循环引用问题创建的
'''
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

db = SQLAlchemy()
mail = Mail()

