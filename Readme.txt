'''
该项目为web项目, 一个包含后台管理与前台访问两部份的bbs论坛
'''

'''
开发环境:
windows 10 家庭版
python 3.7
flask 1.0
mysql 8.0.13
memcached 1.4.4
其他依赖库见Requirements.txt
'''

'''
目录结构:
各文件内有更详细的注释
bbs: 总目录
    app: 主要功能模块, 分为cms\common\front三部分
        cms: 后台管理模块
            forms.py: 表单验证模块
            hooks.py: 钩子函数
            models.py: 模型, 通过sqlachemy映射到数据库中
            utils.py: 一些工具函数
            view.py: 视图函数
        common: 公共模块
            略,基本与cms一致
        front: 前台访问模块
            略,基本与cms一致
    migrations: migrate生成的数据库版本管理模块, versions为更新过的版本, 详情见更新日志
    static: 一些静态文件, 包括css与js, 以及一些图片和视频等
    templates: html文件
    utils: 一些工具的接口, 如memcached, restful等
    vene: 运行环境
    config.py: 配置文件
    exts.py: 避免循环引用
    main.py: 程序运行入口
    manager.py: 终端命令配置文件
    test.py: 仅调试用
'''





