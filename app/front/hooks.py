from .views import bp
from flask import session, g, render_template
from .utils import search_user_by_id
from .models import FrontUser
from ..common.models import Board, Post
import config


@bp.before_request
def current_fuser_for_views():
    # 请求开始前, 将当前用户绑定到g函数上, 以便视图函数中使用
    id = session.get(config.CURRENT_FRONT_USER_ID)
    if id:
        user = search_user_by_id(id)
        g.fuser = user

@bp.context_processor
def current_fuser_for_html():
    # 模板渲染前, 将g函数上的用户传入模板中, 以便在html中使用
    if hasattr(g, 'fuser'):
        return {'current_fuser': g.fuser}
    else:
        return {}


@bp.context_processor
def params_for_html():
    # 模板渲染前, 将一些参数如版块名称等传入模板, 以便在前端页面进行调用
    boards = Board.query.all()
    context = {
        'boards': boards,
    }
    return context

@bp.errorhandler(404)
def page_not_found(error):
    return render_template('front/404.html'), 404