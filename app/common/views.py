from flask import Blueprint, render_template, make_response, request, jsonify
from utils.img_captcha import Captcha
from io import BytesIO
from utils import cache, restful, sms_sender
import qiniu
import config

bp = Blueprint(name='common', import_name=__name__, url_prefix='/common')


@bp.route('/')
def home():
    return 'common'


@bp.route('/captcha/')
def graph_captcha():
    text,image = Captcha.gene_graph_captcha()
    cache.set(text.lower(),text.lower())
    out = BytesIO()
    image.save(out,'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp


@bp.route('/sms_captcha/', methods=['POST'])
def sms_captcha():
    mobile = request.args.get('mobile')
    print(mobile)
    captcha = Captcha.gene_text(4)
    if sms_sender.send(mobile, captcha):
        cache.set(mobile, captcha.lower())
        print(mobile,  captcha)
        return restful.success(message='短信发送成功！5分钟内有效！')
    else:
        return restful.params_error(message='短信发送失败，请稍后重试！')


@bp.route('/uptoken/')
def uptoken():
    access_key = config.QINIU_ACCESS_KEY
    secret_key = config.QINIU_SECRET_KEY
    q = qiniu.Auth(access_key,secret_key)

    bucket = config.QINIU_BUCKET_NAME
    token = q.upload_token(bucket)
    return jsonify({'uptoken':token})
