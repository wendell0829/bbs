import enum

class CMSAuthority(enum.Enum):
    # 全部权限：255的二进制方式来表示 1111 1111
    ALL_PERMISSION = 0b11111111
    # 1. 访问者权限
    VISITOR = 0b00000001
    # 2. 管理帖子权限
    POSTER = 0b00000010
    # 3. 管理评论的权限
    COMMENTER = 0b00000100
    # 4. 管理板块的权限
    BOARDER = 0b00001000
    # 5. 管理前台用户的权限
    FRONTUSER = 0b00010000
    # 6. 管理后台用户的权限
    CMSUSER = 0b00100000
    # 7. 管理后台管理员的权限
    ADMINER = 0b01000000


print(CMSAuthority.VISITOR, type(CMSAuthority.VISITOR))
print(CMSAuthority.VISITOR.value, type(CMSAuthority.VISITOR.value))
print(CMSAuthority(0b00000001))