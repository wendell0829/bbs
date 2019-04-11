'''
该文件为cms用户的视图函数界面, 使用蓝图, 注意蓝图中url_for(如cms.home)中要有蓝图名前缀, url前缀为/cms
包含login_required装饰器的函数为需要登录后才能访问的界面
'''
from flask import Blueprint, render_template, views, redirect, request, url_for, session, g
from .forms import LoginForm, ResetPwdForm, ResetEmailForm
from ..common.forms import BannerForm, UpdateBannerForm, BoardForm, UpdateBoardForm
from .utils import login_check, login_required, update_user, create_captcha_email, authority_required
import config
from utils import restful, cache
from exts import mail
import logging
from .models import CMSAuthority, CMSUser
from ..common.models import Banner, db, Board, Post, StickyRecord, Comment, LikeRecord
from flask_paginate import Pagination, get_page_parameter



bp = Blueprint(name='cms', import_name=__name__, url_prefix='/cms')


@bp.route('/')
@login_required
def home():
    # 首页
    noauthority= request.args.get('noauthority')
    return render_template('cms/home.html', noauthority=noauthority)


@bp.route('/logout/')
@login_required
def logout():
    # 注销, 即在session中删除登录信息
    session.pop(config.CURRENT_CMS_USER_ID)
    return redirect(url_for('cms.login'))


@bp.route('/profile/')
@login_required
def profile():
    # 个人信息页面
    return render_template('cms/profile.html')


@bp.route('/captcha/')
@login_required
def captcha():
    '''
    发送验证码的页面
    跳转到该页面时url中应该包含email参数, 即接收人, 否则(即email为None)跳转到主页
    发送验证码后要将验证码存入memcached中
    :return:
    '''
    email = request.args.get('email')
    if not email:
        return redirect(url_for('cms.home'))
    msg, captcha = create_captcha_email(email)
    try:
        mail.send(msg)
        cache.set(email, captcha)
        return restful.success('邮件已发送，请注意查收！')
    except Exception as e:
        logging.exception(e)
        return restful.server_error('发送失败，请检查您的网络环境！')


class LoginView(views.MethodView):
    '''
    登录页面
    GET　:　注意当用户因为未登录而跳转至此页面时(即因为login_required装饰器), 传入onlogin参数, 在前端alert请先登录
    POST :  1.  先进行表单验证, 然后后台验证密码, 如无问题则将user_id记录在session中;
            2. 注意如果勾选了记住我, 将session的存储周期开启
    '''
    def get(self, message=None):
        onlogin = request.args.get('onlogin')
        return render_template('cms/login.html', message=message, onlogin=onlogin)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            message, current_user = login_check(email, password)
            if message:
                return self.get(message=message)
            else:
                session[config.CURRENT_CMS_USER_ID] = current_user.id
                if remember:
                    session.permanent = True
                return redirect(url_for('cms.home'))
        else:
            message = form.get_error()
            return self.get(message=message)


class ResetPwdView(views.MethodView):
    '''
    重置密码页面
    '''
    decorators = [login_required]

    def get(self):
        return render_template('cms/resetpwd.html')

    def post(self):
        form = ResetPwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            current_user = g.cuser
            if current_user.check_password(oldpwd):
                update_user(user=current_user, password=newpwd)
                return restful.success()
            else:
                return restful.params_error("旧密码错误！")
        else:
            return restful.params_error(form.get_error())


class ResetEmailView(views.MethodView):
    '''
    重置邮箱页面
    '''
    decorators = [login_required]

    def get(self):
        return render_template('cms/resetemail.html')

    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            user = g.cuser
            update_user(user=user, email=email)
            return restful.success('邮箱修改成功！')
        else:
            return restful.params_error(form.get_error())


@bp.route('/posts/')
@login_required
@authority_required(CMSAuthority.POSTER)
def posts():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * config.PER_PAGE
    end = start + config.PER_PAGE
    query_obj = Post.query.order_by(Post.create_time.desc())
    _posts = query_obj.slice(start, end)
    total = query_obj.count()
    pagination = Pagination(bs_version=3, page=page, total=total, outer_window=0, inner_window=2)
    return render_template('cms/posts.html', posts=_posts, pagination=pagination)


@bp.route('/delete_post/', methods=['POST'])
@login_required
@authority_required(CMSAuthority.POSTER)
def delete_post():
    post_id = request.form.get('post_id')
    if not post_id:
        return restful.params_error('参数错误，请稍后重试或联系管理员！')

    post = Post.query.get(post_id)
    if not post:
        return restful.params_error('帖子不存在！')

    db.session.delete(post)
    db.session.commit()
    return restful.success('帖子删除成功！')


@bp.route('/stick_post/', methods=['POST'])
@login_required
@authority_required(CMSAuthority.POSTER)
def stick_post():
    post_id = request.form.get('post_id')
    to_do = request.form.get('to_do')
    if not post_id:
        return restful.params_error('参数错误，请稍后重试或联系管理员！')

    post = Post.query.get(post_id)
    if not post:
        return restful.params_error('帖子不存在！')
    if to_do == '1':
        sticky = StickyRecord()
        sticky.operator = g.cuser
        sticky.post = post
        db.session.add(sticky)
    elif to_do == '0':
        sticky = StickyRecord.query.filter_by(post_id=post_id).one()
        db.session.delete(sticky)
    else:
        return restful.params_error('参数错误，请稍后重试或联系管理员！')
    db.session.commit()
    return restful.success('操作成功！')


@bp.route('/comments/')
@login_required
@authority_required(CMSAuthority.COMMENTER)
def comments():
    return render_template('cms/comments.html')


@bp.route('/boards/')
@login_required
@authority_required(CMSAuthority.BOARDER)
def boards():
    _boards = Board.query.order_by(Board.create_time.desc()).all()
    return render_template('cms/boards.html', boards=_boards)


@bp.route('/add_board/', methods=['POST'])
@login_required
@authority_required(CMSAuthority.BOARDER)
def add_board():
    form = BoardForm(request.form)
    if form.validate():
        name = form.name.data
        moderator_email = form.moderator_email.data
        moderator = CMSUser.query.filter_by(email=moderator_email).one()
        desc = form.desc.data
        board = Board(name=name, desc=desc, moderator=moderator, cms_user_id=moderator.id)

        db.session.add(board)
        db.session.commit()
        return restful.success(message='板块添加成功!')
    else:
        error = form.get_error()
        return restful.params_error(message=error)


@bp.route('/delete_board/', methods=['POST'])
@login_required
@authority_required(CMSAuthority.BOARDER)
def delete_board():
    try:
        board_id = request.form.get('board_id')
        board = Board.query.filter_by(id=board_id).one_or_none()
        db.session.delete(board)
        db.session.commit()
        return restful.success(message='该版块已被删除！')
    except:
        return restful.params_error(message='删除失败，请稍后再试或联系管理员！')


@bp.route('/update_board/', methods=['POST'])
@login_required
@authority_required(CMSAuthority.BOARDER)
def update_board():
    form = UpdateBoardForm(request.form)
    if form.validate():
        board_id = form.board_id.data
        moderator_email = form.moderator_email.data
        moderator = CMSUser.query.filter_by(email=moderator_email).one()
        board = Board.query.filter_by(id=board_id).one()
        board.name = form.name.data
        board.moderator = moderator
        board.cms_user_id = moderator.id
        board.desc = form.desc.data

        db.session.commit()
        return restful.success(message='修改成功！')
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/fusers/')
@login_required
@authority_required(CMSAuthority.FRONTUSER)
def fusers():
    return render_template('cms/fusers.html')


@bp.route('/froles/')
@login_required
@authority_required(CMSAuthority.FRONTUSER)
def froles():
    return render_template('cms/froles.html')


@bp.route('/cusers/')
@login_required
@authority_required(CMSAuthority.CMSUSER)
def cusers():
    return render_template('cms/cusers.html')


@bp.route('/croles/')
@login_required
@authority_required(CMSAuthority.CMSUSER)
def croles():
    return render_template('cms/croles.html')


@bp.route('/banners/')
@login_required
@authority_required(CMSAuthority.POSTER)
def banners():
    _banners = Banner.query.order_by(Banner.create_time.desc()).all()
    return render_template('cms/banners.html', banners=_banners)


@bp.route('/add_banner/', methods=['POST'])
@login_required
@authority_required(CMSAuthority.POSTER)
def add_banner():
    form = BannerForm(request.form)
    if form.validate():
        name = form.name.data
        img_url = form.img_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = Banner(name=name, img_url=img_url, link_url=link_url, priority=priority)

        g.cuser.banners.append(banner)
        db.session.commit()
        return restful.success(message='{}添加轮播图成功'.format(g.cuser.name))
    else:
        error = form.get_error()
        return restful.params_error(message=error)


@bp.route('/delete_banner/', methods=['POST'])
@login_required
@authority_required(CMSAuthority.POSTER)
def delete_banner():
    try:
        banner_id = request.form.get('banner_id')
        banner = Banner.query.filter_by(id=banner_id).one_or_none()
        db.session.delete(banner)
        db.session.commit()
        return restful.success(message='该轮播图已被删除！')
    except:
        return restful.params_error(message='删除失败，请稍后再试或联系管理员！')


@bp.route('/update_banner/', methods=['POST'])
@login_required
@authority_required(CMSAuthority.POSTER)
def update_banner():
    form = UpdateBannerForm(request.form)
    if form.validate():
        banner_id = form.banner_id.data
        banner = Banner.query.filter_by(id=banner_id).one()
        banner.name = form.name.data
        banner.img_url = form.img_url.data
        banner.link_url = form.link_url.data
        banner.priority = form.priority.data
        banner.creater = g.cuser
        db.session.commit()
        return restful.success(message='修改成功！')
    else:
        return restful.params_error(message=form.get_error())


bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpwd/', view_func=ResetPwdView.as_view('resetpwd'))
bp.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))


