from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from main import create_app
from exts import db
from app.cms import models as cms_models

CMSUser = cms_models.CMSUser
CMSRole = cms_models.CMSRole
CMSAuthority = cms_models.CMSAuthority

app = create_app()

manager = Manager(app)

Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.option('-n', '--name', dest='name')
@manager.option('-p', '--password', dest='password')
@manager.option('-ph', '--phone', dest='phone')
def add_cms_user(name, password, phone):
    user = CMSUser(name=name, password=password, phone=phone)
    db.session.add(user)
    db.session.commit()
    print('cms用户添加成功！')


@manager.command
def create_role():
    print(type(CMSAuthority.VISITOR))
    # 1. 访问者（可以修改个人信息）
    visitor = CMSRole(name='访问者',desc='只能查看相关数据，不能修改。')
    visitor.authority = CMSAuthority.VISITOR

    # 2. 运营角色（修改个人个人信息，管理帖子，管理评论，管理前台用户）
    operator = CMSRole(name='运营',desc='管理帖子，管理评论,管理前台用户。')
    operator.authority = CMSAuthority.VISITOR|CMSAuthority.POSTER|CMSAuthority.CMSUSER|CMSAuthority.COMMENTER|CMSAuthority.FRONTUSER

    # 3. 管理员（拥有绝大部分权限）
    admin = CMSRole(name='管理员',desc='拥有本系统所有权限。')
    admin.authority = CMSAuthority.VISITOR|CMSAuthority.POSTER|CMSAuthority.CMSUSER|CMSAuthority.COMMENTER|CMSAuthority.FRONTUSER|CMSAuthority.BOARDER

    # 4. 开发者
    developer = CMSRole(name='开发者',desc='开发人员专用角色。')
    developer.authority = CMSAuthority.ALL_PERMISSION

    db.session.add_all([visitor,operator,admin,developer])
    db.session.commit()
    print('角色创建成功！')

@manager.option('-n', '--name', dest='name')
@manager.option('-ph', '--phone', dest='phone')
def add_user_to_role(name, phone):
    user = db.session.query(CMSUser).filter_by(phone=phone).first()

    if user:
        role = db.session.query(CMSRole).filter_by(name=name).first()
        if role:
            role.users.append(user)
            db.session.commit()
            print('成功！用户（{}）已添加到角色（{}）中'.format(phone, name))
        else:
            print('该角色模型（{}）不存在'.format(name))
    else:
        print('该用户（{}）不存在'.format(phone))

@manager.option('-a', '--authority', dest='authority')
@manager.option('-ph', '--phone', dest='phone')
def test_permission(authority, phone):
    user = db.session.query(CMSUser).filter_by(phone=phone).first()
    authority = int(authority)
    if user:
        if user.check_authority(authority):
            print('用户{}拥有权限{}'.format(phone, authority))
        else:
            print('用户{}没有权限{}'.format(phone, authority))
    else:
        print('用户不存在!')



if __name__ == '__main__':
    manager.run()
