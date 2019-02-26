from flask import Blueprint, render_template

bp = Blueprint(name='front', import_name=__name__)


@bp.route('/')
def home():
    return 'front'
