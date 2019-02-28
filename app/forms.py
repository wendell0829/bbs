from wtforms import Form


class BaseForm(Form):
    '''
    基本的验证表单类型, 可以用来定义一些表单验证需要用到的通用方法, 比如取error
    '''
    def get_error(self):
        '''
        从错误中取出一个, 以便在模板中渲染以提醒客户
        :return:
        '''
        return self.errors.popitem()[1][0]