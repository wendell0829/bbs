from flask import Blueprint, render_template, views, request, session, url_for, g, redirect, abort
from .forms import SingupForm, SigninForm, AvatarForm
from .utils import add_front_user, check_mobile, login_required
from utils import restful, safeutils
from config import CURRENT_FRONT_USER_ID, PER_PAGE
from ..common.models import Banner, Post, db, Board, Comment, LikeRecord, StickyRecord
from ..common.forms import PostForm, CommentForm
from flask_paginate import Pagination, get_page_parameter


bp = Blueprint(name='front', import_name=__name__)
   

@bp.route('/')
def home():
    board_id = request.args.get('board_id', type=int, default=None)
    sort_id = request.args.get('sort_id', type=int, default=0)
    banners = Banner.query.order_by(Banner.priority.desc()).limit(3)
    posts = None
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page-1)*PER_PAGE
    end = start + PER_PAGE
    total = 0
    query_obj = None

    if sort_id == 0:
        query_obj = Post.query.order_by(Post.create_time.desc())
        posts = query_obj.slice(start, end)
        total = query_obj.count()
    elif sort_id == 1:
        query_obj = db.session.query(Post).outerjoin(LikeRecord).group_by(Post.id).order_by(db.func.count(LikeRecord.id).desc(), Post.create_time.desc())
        posts = query_obj.slice(start, end)
        total = query_obj.count()
    elif sort_id == 2:
        query_obj = db.session.query(Post).outerjoin(Comment).group_by(Post.id).order_by(db.func.count(Comment.id).desc(), Post.create_time.desc())
        posts = query_obj.slice(start, end)
        total = query_obj.count()
    elif sort_id == 3:
        query_obj = db.session.query(Post).outerjoin(StickyRecord).order_by(StickyRecord.operate_time.desc(), Post.create_time.desc())
        posts = query_obj.slice(start, end)
        total = query_obj.count()
    else:
        abort(404)

    if board_id:
        board = Board.query.filter_by(id=board_id).one_or_none()
        if board:
            query_obj = query_obj.filter_by(board_id=board_id).order_by(Post.create_time.desc())
            posts = query_obj.slice(start, end)
            total = query_obj.count()
        else:
            abort(404)

    pagination = Pagination(bs_version=3,page=page,total=total,outer_window=0,inner_window=2)
    context = {
        'banners': banners,
        'board_id': board_id,
        'posts': posts,
        'pagination': pagination,
        'sort_id': sort_id
    }
    return render_template('front/home.html', **context)


@bp.route('/signout/')
def signout():
    session.pop(CURRENT_FRONT_USER_ID)
    return redirect(url_for('front.signin'))


@bp.route('/like/', methods=['POST'])
def like():
    post_id = request.form.get('post_id')
    to_do = request.form.get('to_do')
    if not post_id:
        return restful.params_error('参数错误，请稍后重试或联系管理员！')

    post = Post.query.get(post_id)
    if not post:
        return restful.params_error('帖子不存在！')
    if to_do == '1':
        like = LikeRecord()
        like.post = post
        if like.operator == g.fuser:
            return restful.params_error('您已点过赞了！')
        like.operator = g.fuser
        db.session.add(like)
    elif to_do == '0':
        like = LikeRecord.query.filter_by(post_id=post_id).filter_by(operator_id=g.fuser.id).one()
        db.session.delete(like)
    else:
        return restful.params_error('参数错误，请稍后重试或联系管理员！')
    db.session.commit()
    return restful.success('操作成功！')

@bp.route('/post/<post_id>')
@login_required
def post_detail(post_id):
    post = Post.query.filter_by(id=post_id).one_or_none()
    # star_author_ids = [star_model.author.id for star_model in post_model.stars]
    like_records = LikeRecord.query.filter_by(post_id=post_id).all()
    liker_ids = [like_record.operator_id for like_record in like_records ]
    if post:
        return render_template('front/post_detail.html', post=post, liker_ids=liker_ids)
    else:
        abort(status=404)


@bp.route('/add_comment/', methods=['POST'])
@login_required
def add_comment():
    form = CommentForm(request.form)
    if form.validate():
        content = form.content.data
        post_id = form.post_id.data
        post = Post.query.get(post_id)
        comment = Comment(content=content)
        comment.post = post
        comment.author = g.fuser
        db.session.add(comment)
        db.session.commit()
        return restful.success(message='评论提交成功！')
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/add_avatar/', methods=['POST'])
@login_required
def add_avatar():
    form = AvatarForm(request.form)
    if form.validate():
        avatar = form.avatar.data
        g.fuser.avatar = avatar
        db.session.commit()
        return restful.success(message='头像上传成功！')
    else:
        error = form.get_error()
        return restful.params_error(message=error)


@bp.route('/profile')
@login_required
def profile():
    return render_template('front/profile.html')

class SignupView(views.MethodView):
    def get(self):
        return render_template('front/signup.html')

    def post(self):
        form = SingupForm(request.form)
        if form.validate():
            mobile = form.mobile.data
            if check_mobile(mobile):
                return restful.params_error(message='该手机号已注册！')
            else:
                username = form.username.data
                password = form.password1.data
                try:
                    add_front_user(username=username, password=password, mobile=mobile)
                except:
                    return restful.params_error(message='注册失败，请稍后重试！')
                return restful.success(message='注册成功！')
        else:
            error = form.get_error()
            return restful.params_error(message=error)


class SigninView(views.MethodView):
    def get(self):
        return_to = request.referrer[15:].split('?')[0]
        onlogin = request.args.get('onlogin')
        if (return_to and
            return_to != url_for('front.signup') and
            safeutils.is_safe_url(return_to) and
            return_to != url_for('front.signin')
        ):
            return render_template('front/signin.html', return_to=return_to, onlogin=onlogin)
        else:
            return render_template('front/signin.html')

    def post(self):
        form = SigninForm(request.form)
        user = form.validate()
        if user:
            remember = form.remember.data
            session[CURRENT_FRONT_USER_ID] = user.id
            if remember:
                session.permanent = True
            return restful.success(message='登录成功！')
        else:
            error = form.get_error()
            return restful.params_error(message=error)


class AddPostView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('front/add_post.html')

    def post(self):
        form = PostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            author = g.fuser
            _post = Post(title=title, content=content, board_id=board_id, author=author)

            db.session.add(_post)
            db.session.commit()

            return restful.success(message='帖子发布成功！')

        else:
            return restful.params_error(form.get_error())






@bp.route('/test/')
def test():
    return render_template('front/test.html')


bp.add_url_rule('/signup/', view_func=SignupView.as_view('signup'))
bp.add_url_rule('/signin/', view_func=SigninView.as_view('signin'))
bp.add_url_rule('/add_post/', view_func=AddPostView.as_view('add_post'))