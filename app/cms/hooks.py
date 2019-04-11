'''
该文件为一些钩子函数, 利用g函数传递一些参数
'''
from .views import bp
from flask import session, g
from .utils import search_user_by_id
from .models import CMSAuthority
import config

@bp.before_request
def current_cuser_for_views():
    # 请求开始前, 将当前用户绑定到g函数上, 以便视图函数中使用
    id = session.get(config.CURRENT_CMS_USER_ID)
    if id:
        user = search_user_by_id(id)
        g.cuser = user


@bp.context_processor
def current_cuser_for_html():
    # 模板渲染前, 将g函数上的用户传入模板中, 以便在html中使用
    if hasattr(g, 'cuser'):
        return {'current_cuser': g.cuser}
    else:
        return {}


@bp.context_processor
def authority_for_html():
    # 模板渲染前, 将权限模型传入模板, 以便在前端页面进行权限验证
    return {'authority' : CMSAuthority}



