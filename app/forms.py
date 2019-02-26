from wtforms import Form


class BaseForm(Form):
    def get_errors(self):
        return self.errors.popitem()[1][0]