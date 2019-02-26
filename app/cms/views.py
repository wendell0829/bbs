from flask import Blueprint, render_template, views, redirect, request, url_for, session, g
from .forms import LoginForm, ResetPwdForm, ResetEmailForm
from .utils import login_check, login_required, update_user, create_captcha
import config
from utils import restful, cache
from exts import mail
import logging

bp = Blueprint(name='cms', import_name=__name__, url_prefix='/cms')

@bp.route('/')
@login_required
def home():
    return render_template('cms/home.html')


@bp.route('/logout/')
@login_required
def logout():
    session.pop(config.CURRENT_USER_ID)
    return redirect(url_for('cms.login'))


@bp.route('/profile/')
@login_required
def profile():
    return render_template('cms/profile.html')


@bp.route('/captcha/')
@login_required
def captcha():
    email = request.args.get('email')
    msg, captcha= create_captcha(email)
    try:
        mail.send(msg)
        cache.set(email, captcha)
        return restful.success('邮件已发送，请注意查收！')
    except Exception as e:
        logging.exception(e)
        return restful.server_error('发送失败，请检查您的网络环境！')



class LoginView(views.MethodView):
    def get(self, message=None):
        onlogin = request.args.get('onlogin')
        return render_template('cms/login.html', message=message, onlogin=onlogin)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            phone = form.phone.data
            password = form.password.data
            remember = form.remember.data
            message, current_user = login_check(phone, password)
            if message:
                return self.get(message=message)
            else:
                session[config.CURRENT_USER_ID] = current_user.id
                if remember:
                    session.permanent = True
                return redirect(url_for('cms.home'))
        else:
            message = form.get_errors()
            return self.get(message=message)


class ResetPwdView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('cms/resetpwd.html')

    def post(self):
        form = ResetPwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            current_user = g.user
            if current_user.check_password(oldpwd):
                update_user(user=current_user, password=newpwd)
                return restful.success()
            else:
                return restful.params_error("旧密码错误！")
        else:
            return restful.params_error(form.get_errors())


class ResetEmailView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('cms/resetemail.html')

    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            user = g.user
            update_user(user=user, email=email)
            return restful.success('邮箱修改成功！')
        else:
            return restful.params_error(form.get_errors())


bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpwd/', view_func=ResetPwdView.as_view('resetpwd'))
bp.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))


