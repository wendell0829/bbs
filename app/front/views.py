from flask import Blueprint, render_template, views, request, session
from .forms import SingupForm
from .utils import add_front_user, check_mobile
from utils import restful
from config import CURRENT_USER_ID


bp = Blueprint(name='front', import_name=__name__)


@bp.route('/')
def home():
    return 'front'

@bp.route('/test/')
def test():
    return render_template('front/test.html')

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
                    current_user = add_front_user(username=username, password=password, mobile=mobile)
                except:
                    return restful.params_error(message='注册失败，请稍后重试！')
                session[CURRENT_USER_ID] = current_user.id
                return restful.success(message='注册成功！')
        else:
            error = form.get_error()
            return restful.params_error(message=error)


bp.add_url_rule('/signup/', view_func=SignupView.as_view('signup'))