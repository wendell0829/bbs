import requests
import config

def send(mobie, sms_captcha):
    url = config.URL
    params = {
        "mobile": mobie,  # 接受短信的用户手机号码
        "tpl_id": config.TPL_ID,  # 您申请的短信模板ID，根据实际情况修改
        "tpl_value": "#code#=" + sms_captcha,  # 您设置的模板变量，根据实际情况修改
        "key": config.APP_KEY,  # 应用APPKEY(应用详细页查询)
    }

    res = requests.get(url, params).json()
    print(res, res.get('error_code'))
    if res.get('error_code') == 0:
        return True
    else:
        return False