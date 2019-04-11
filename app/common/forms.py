from ..forms import BaseForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, ValidationError, Length
from .models import Banner, Post, Board
from ..cms.models import CMSUser


class BannerForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入图片名称！'),
                                   Length(max=30, message='图片名称过长！')])
    img_url = StringField(validators=[InputRequired(message='请输入图片链接！')])
    link_url = StringField(validators=[InputRequired(message='请输入图片跳转链接！')])
    priority = IntegerField(validators=[InputRequired(message='请输入图片优先级！')])

    def validate_name(self, filed):
        name = filed.data
        if Banner.query.filter_by(name=name).one_or_none():
            raise ValidationError(message='该图片名称已存在！')


class UpdateBannerForm(BannerForm):
    banner_id = IntegerField(validators=[InputRequired(message='没有轮播图id信息！')])

    def validate_name(self, filed):
        pass

    def validate(self):
        if not super(BannerForm,self).validate():
            return False

        banner = Banner.query.filter_by(id=self.banner_id.data).one_or_none()
        if banner:
            if(banner.name == self.name.data and
            banner.img_url == self.img_url.data and
            banner.link_url == self.link_url.data and
            banner.priority == self.priority.data):
                self.banner_id.errors.append('未检测到变化，请至少改变一个参数！')
                return False
            else:
                return True
        else:
            self.banner_id.errors.append('修改失败，请稍后重试或联系管理员！')


class BoardForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入板块名称！'),
                                   Length(max=30, message='板块名称过长！')])
    moderator_email = StringField(validators=[InputRequired(message='请输入版主邮箱！')])
    desc = StringField(validators=[Length(max=99, message='描述过长，请不要超过99个字符！')])

    def validate_name(self, filed):
        name = filed.data
        if Board.query.filter_by(name=name).one_or_none():
            raise ValidationError(message='该版块名称已存在！')

    def validate_moderator_email(self, filed):
        moderator = CMSUser.query.filter_by(email=filed.data).one_or_none()
        if not moderator:
            raise ValidationError(message='该邮箱未绑定到cms用户，请检查！')


class UpdateBoardForm(BoardForm):
    board_id = IntegerField(validators=[InputRequired(message='没有版块id信息！')])

    def validate_name(self, filed):
        pass

    def validate(self):
        if not super(BoardForm, self).validate():
            return False

        board = Board.query.filter_by(id=self.board_id.data).one_or_none()
        if board:
            if (board.name == self.name.data and
                    board.moderator.email == self.moderator_email.data and
                    board.desc == self.desc.data):
                self.board_id_id.errors.append('未检测到变化，请至少改变一个参数！')
                return False
            else:
                return True
        else:
            self.board_id.errors.append('修改失败，请稍后重试或联系管理员！')


class PostForm(BaseForm):
    title = StringField(validators=[InputRequired(message='请输入标题！'),
                                    Length(max=30, message='标题长度不得超过30个字符！')])

    content = StringField(validators=[InputRequired(message='文章内容不能为空！')])
    board_id = IntegerField(validators=[InputRequired(message='未选择板块！')])

    def validate_board_id(self, field):
        board = Board.query.filter_by(id=field.data).one_or_none()
        if not board:
            raise ValidationError(message='板块参数有错误，请稍后再试或联系管理员！')


class CommentForm(BaseForm):
    content = StringField(validators=[InputRequired(message='评论内容不能为空！')])
    post_id = IntegerField(validators=[InputRequired(message='帖子参数有错误，请稍后再试或联系管理员！')])

    def validate_post_id(self, field):
        post = Post.query.get(field.data)
        if not post:
            raise ValidationError(message='帖子参数有错误，请稍后再试或联系管理员！')