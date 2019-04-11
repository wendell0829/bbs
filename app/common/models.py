from exts import db
from datetime import datetime


class Banner(db.Model):
    __tablename__ = 'banner'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(99), nullable=False, unique=True)
    img_url = db.Column(db.String(255), nullable=False)
    link_url = db.Column(db.String(255), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    priority = db.Column(db.Integer, default=0)
    cms_user_id = db.Column(db.Integer, db.ForeignKey('cms_user.id'), nullable=False)
    creater = db.relationship('CMSUser', backref='banners')


class Board(db.Model):
    __tablename__ = 'board'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    desc = db.Column(db.String(99))
    create_time = db.Column(db.DateTime, default=datetime.now)
    cms_user_id = db.Column(db.Integer, db.ForeignKey('cms_user.id'), nullable=False)
    moderator = db.relationship('CMSUser', backref='boards')


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(30), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))
    board = db.relationship('Board', backref='posts')

    author_id = db.Column(db.String(25), db.ForeignKey('front_user.id'))
    author = db.relationship('FrontUser', backref='posts')


class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', backref='comments')

    author_id = db.Column(db.String(25), db.ForeignKey('front_user.id'))
    author = db.relationship('FrontUser', backref='comments')


class StickyRecord(db.Model):
    __tablename__ = 'sticky_record'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    operate_time = db.Column(db.DateTime, default=datetime.now)

    operator_id = db.Column(db.Integer, db.ForeignKey('cms_user.id'))
    operator = db.relationship('CMSUser', backref='sticky_records')

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', backref='sticky')


class LikeRecord(db.Model):
    __tablename__ = 'like_record'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    operate_time = db.Column(db.DateTime, default=datetime.now)

    operator_id = db.Column(db.String(25), db.ForeignKey('front_user.id'))
    operator = db.relationship('FrontUser', backref='like_records')

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', backref='like_records')
