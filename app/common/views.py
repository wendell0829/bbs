from flask import Blueprint, render_template

bp = Blueprint(name='common', import_name=__name__, url_prefix='/common')


@bp.route('/')
def home():
    return 'common'
