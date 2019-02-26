from .views import bp, session, g
from .utils import search_user_of_id
import config

@bp.before_request
def current_user_for_views():
    id = session.get(config.CURRENT_USER_ID)
    if id:
        user = search_user_of_id(id)
        g.user = user


@bp.context_processor
def current_user_for_html():
    if hasattr(g, 'user'):
        return {'current_user': g.user}
    else:
        return {}



