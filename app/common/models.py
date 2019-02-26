# from exts import db
# import enum
# from werkzeug.security import generate_password_hash, check_password_hash
# from datetime import datetime
#
#
# class AuthorityEnum(enum.Enum):
#     SUPER_ADMINISTRATOR = 0
#     ADMINISTRATOR = 1
#     User = 9
#
#
# class User(db.Model):
#     __tablename__ = 'cms_user'
#
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(20), nullable=False)
#     _password = db.Column(db.String(200), nullable=False)
#     phone = db.Column(db.String(15), nullable=False, unique=True)
#     jointime = db.Column(db.DateTime, default=datetime.now)
#     authority = db.Column(db.Enum(AuthorityEnum), default=0)
#
#     def __init__(self, name, password, phone):
#         self.name = name
#         self.phone = phone
#         self.password = password
#
#
#     @property
#     def password(self):
#         return self._password
#
#     @password.setter
#     def password(self, raw_password):
#         self._password = generate_password_hash(raw_password)
#
#     def check_password(self, raw_password):
#         result = check_password_hash(self.password, raw_password)
#         return result