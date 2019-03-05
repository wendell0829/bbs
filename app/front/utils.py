from .models import FrontUser, db


def add_front_user(username, password, mobile):
    user = FrontUser(username=username, password=password, mobile=mobile)

    db.session.add(user)
    db.session.commit()

    print(user.id)
    return user


def check_mobile(mobile):
    user = FrontUser.query.filter_by(mobile=mobile).one_or_none()
    if user:
        return True
    else:
        return False