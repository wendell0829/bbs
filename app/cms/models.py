'''
该文件为cms用户模型, 通过sqlachemy映射至sql数据库中
'''
from exts import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
# import enum

class CMSAuthority(object):
    '''
    该类为角色权限，注意如果使用枚举类的话，取值时需要使用CMSSAuthority.VISITOR.value的形式，
    即需要额外加一个.value，为了避免麻烦，这里不使用。
    '''
    # 全部权限：255的二进制方式来表示 1111 1111
    ALL_PERMISSION = 0b11111111
    # 1. 访问者权限
    VISITOR = 0b00000001
    # 2. 管理帖子权限
    POSTER = 0b00000010
    # 3. 管理评论的权限
    COMMENTER = 0b00000100
    # 4. 管理板块的权限
    BOARDER = 0b00001000
    # 5. 管理前台用户的权限
    FRONTUSER = 0b00010000
    # 6. 管理后台用户的权限
    CMSUSER = 0b00100000
    # 7. 管理后台管理员的权限
    ADMINER = 0b01000000

# 下表为角色与用户模型多对多关系的中间表
cms_role_user = db.Table(
    'cms_role_user',
    db.Column('cms_user_id', db.Integer, db.ForeignKey('cms_user.id'), primary_key=True),
    db.Column('cms_role_id', db.Integer, db.ForeignKey('cms_role.id'), primary_key=True),
)


class CMSRole(db.Model):
    '''
    角色模型, 通过将用户加入某个角色, 可以方便的给用户赋予权限
    id: 自增整数
    name: 角色名字, 如游客, 管理员等
    desc: 描述, 如 只有浏览权限等
    authorities: 权限, 整型, 创建时通过权限模型赋值, 默认为访客
    creat_time: 创建时间
    users: 该模型下所有的用户, 通过backref, 用户可以通过roles获取其角色
    '''
    __tablename__ = 'cms_role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    desc = db.Column(db.String(200), nullable=True)
    authority = db.Column(db.Integer, default=CMSAuthority.VISITOR)
    creat_time = db.Column(db.DateTime, default=datetime.now)

    users = db.relationship('CMSUser', secondary=cms_role_user, backref='roles')


class CMSUser(db.Model):
    '''
    cms用户模型
    id: 自增整数
    name: 用户名
    _password: 密码, 为了保证安全, 数据库中不存储原始密码, 使用hash加密后存储
                通过设置类属性封装后, 再通过setter方法在存储前加密
    phone: 注册手机号, 唯一
    email:　注册邮箱, 唯一
    join_time: 注册时间
    '''
    __tablename__ = 'cms_user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    _password = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(30), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, name, password, email, phone=None):
        self.name = name
        self.phone = phone
        self.password = password
        self.email = email


    @property
    def password(self):
        # 通过property将password转化为方法, 以便进行操作后再存储
        return self._password

    @password.setter
    def password(self, raw_password):
        # setter装饰器可以在创建类时取代init
        self._password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)
        return result

    @property
    def authority(self):
        '''
        设置用户权限, 根据用户拥有的角色, 将每个角色的权限取并集
        :return:
        '''
        authority = 0
        if self.roles:
            for a in self.roles:
                authority = a.authority|authority
        return authority

    def check_authority(self, authority):
        # 验证用户是否拥有某个权限, 通过取并的方式, 若拥有, 则取并后应不变
        return self.authority&authority == authority

