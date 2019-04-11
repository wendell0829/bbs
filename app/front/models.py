from exts import db
from datetime import datetime
import enum
import shortuuid
from werkzeug.security import generate_password_hash, check_password_hash
from config import DEFAULT_AVATAR


class GenderEnum(enum.Enum):
    MALE = 1
    FEMALE = 2
    SECRET = 9
    UNKNOWN = 0


class FrontUser(db.Model):
    __tablename__ = 'front_user'

    id = db.Column(db.String(25), primary_key=True, unique=True, default=shortuuid.uuid)
    name = db.Column(db.String(20), nullable=False)
    _password = db.Column(db.String(200), nullable=False)
    mobile = db.Column(db.String(15), nullable=False, unique=True)
    email = db.Column(db.String(30), unique=True)
    gender = db.Column(db.Enum(GenderEnum), default=GenderEnum.UNKNOWN)
    avatar = db.Column(db.String(150), default=DEFAULT_AVATAR)
    signature = db.Column(db.String(50))
    realname = db.Column(db.String(10))
    join_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, *args, **kwargs):
        if 'password' in kwargs:
            self.password = kwargs.get('password')
            kwargs.pop('password')
        super(FrontUser, self).__init__(*args, **kwargs)


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


