class User():
    def __init__(self, *args, **kwargs):
        if 'password' in kwargs:
            self.password = kwargs.get('password')
            kwargs.pop('password')
        super(User, self).__init__(*args, **kwargs)


user = User(name='test1', password='111111')
print(user.name)
print(user.password)