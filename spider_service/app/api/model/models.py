# coding: utf-8
from sqlalchemy import Column, DECIMAL, DateTime, String, Text, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, TINYINT, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AuthAction(Base):
    __tablename__ = 'auth_action'

    id = Column(BIGINT(20), primary_key=True, comment='权限操作主键')
    name = Column(String(155), nullable=False, comment='对应英文缩略名')
    description = Column(String(50), nullable=False, comment='对应的名称')
    active = Column(TINYINT(1), server_default=text("'1'"))
    version = Column(INTEGER(11), server_default=text("'0'"))
    gmt_create = Column(DateTime, comment='记录创建时间')
    gmt_modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='记录修改时间')
    create_by = Column(String(255))
    modified_by = Column(String(255))


class AuthPermission(Base):
    __tablename__ = 'auth_permission'

    id = Column(BIGINT(20), primary_key=True)
    name = Column(String(150), nullable=False)
    description = Column(String(255))
    active = Column(TINYINT(1), server_default=text("'1'"))
    version = Column(INTEGER(11), server_default=text("'0'"))
    gmt_create = Column(DateTime)
    gmt_modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    create_by = Column(String(255), nullable=False)
    modified_by = Column(String(255), nullable=False)


class AuthPermissionAction(Base):
    __tablename__ = 'auth_permission_action'

    id = Column(BIGINT(20), primary_key=True)
    permission_id = Column(BIGINT(20))
    action_id = Column(BIGINT(20))
    version = Column(INTEGER(11), server_default=text("'0'"))
    gmt_create = Column(DateTime)
    gmt_modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    create_by = Column(String(255))
    modified_by = Column(String(255))


class AuthRole(Base):
    __tablename__ = 'auth_role'

    id = Column(BIGINT(20), primary_key=True)
    name = Column(String(50))
    description = Column(String(255))
    active = Column(TINYINT(1), server_default=text("'1'"))
    version = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    gmt_create = Column(DateTime)
    gmt_modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    create_by = Column(String(255))
    modified_by = Column(String(255))


class AuthRolePemission(Base):
    __tablename__ = 'auth_role_pemission'

    id = Column(BIGINT(20), primary_key=True)
    role_id = Column(BIGINT(20))
    permission_id = Column(BIGINT(20))
    action_id = Column(BIGINT(20))
    active = Column(TINYINT(1), server_default=text("'1'"))
    version = Column(INTEGER(11), server_default=text("'0'"))
    gmt_create = Column(DateTime)
    gmt_modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    create_by = Column(String(255))
    modified_by = Column(String(255))


class FileUpload(Base):
    __tablename__ = 'file_upload'

    id = Column(BIGINT(20), primary_key=True)
    userid = Column(String(255))
    file_upload_type_id = Column(BIGINT(20))
    session_token = Column(String(255))
    original_filename = Column(String(255))
    filename = Column(String(255))
    path = Column(String(500))
    url = Column(String(500))
    external_parameter = Column(Text)
    active = Column(TINYINT(1), server_default=text("'1'"))
    version = Column(INTEGER(11), server_default=text("'0'"))
    gmt_create = Column(DateTime)
    gmt_modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    create_by = Column(String(255))
    modified_by = Column(String(255))


class FileUploadType(Base):
    __tablename__ = 'file_upload_type'

    id = Column(BIGINT(20), primary_key=True)
    name = Column(String(50))
    description = Column(String(255))
    gmt_create = Column(DateTime)
    gmt_modified = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    create_by = Column(String(255))
    modified_by = Column(String(255))


class SearchHistory(Base):
    __tablename__ = 'search_history'

    id = Column(BIGINT(20), primary_key=True, comment='主键')
    userid = Column(String(255))
    keyword = Column(String(500))
    active = Column(TINYINT(1), nullable=False, server_default=text("'1'"), comment='对应该条记录是否可用，1可用，0不可用')
    version = Column(INTEGER(20), nullable=False, server_default=text("'0'"), comment='对应乐观锁的版本号')
    gmt_create = Column(DateTime, nullable=False, comment='对应记录的创建时间')
    gmt_modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='对应记录的修改时间')
    create_by = Column(String(250), nullable=False, comment='对应添加记录的人')
    modified_by = Column(String(250), nullable=False, comment='对应最后一次修改记录的')


class SearchHistoryHot(Base):
    __tablename__ = 'search_history_hot'

    id = Column(BIGINT(20), primary_key=True, comment='主键')
    keyword = Column(String(500))
    count = Column(BIGINT(20))
    active = Column(TINYINT(1), nullable=False, server_default=text("'1'"), comment='对应该条记录是否可用，1可用，0不可用')
    version = Column(INTEGER(20), nullable=False, server_default=text("'0'"), comment='对应乐观锁的版本号')
    gmt_create = Column(DateTime, nullable=False, comment='对应记录的创建时间')
    gmt_modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='对应记录的修改时间')
    create_by = Column(String(250), nullable=False, comment='对应添加记录的人')
    modified_by = Column(String(250), nullable=False, comment='对应最后一次修改记录的')


class SearchKeyword(Base):
    __tablename__ = 'search_keyword'

    id = Column(BIGINT(20), primary_key=True, comment='主键')
    product_Id = Column(BIGINT(20))
    keyword = Column(String(255))
    active = Column(TINYINT(1), nullable=False, server_default=text("'1'"), comment='对应该条记录是否可用，1可用，0不可用')
    version = Column(INTEGER(20), nullable=False, server_default=text("'0'"), comment='对应乐观锁的版本号')
    gmt_create = Column(DateTime, nullable=False, comment='对应记录的创建时间')
    gmt_modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='对应记录的修改时间')
    create_by = Column(String(250), nullable=False, comment='对应添加记录的人')
    modified_by = Column(String(250), nullable=False, comment='对应最后一次修改记录的')


class SmsVerifyCode(Base):
    __tablename__ = 'sms_verify_code'

    id = Column(BIGINT(20), primary_key=True, comment='主键')
    mobile = Column(DECIMAL(11, 0))
    code = Column(String(255))
    active = Column(TINYINT(1), nullable=False, server_default=text("'1'"), comment='对应该条记录是否可用，1可用，0不可用')
    version = Column(INTEGER(20), nullable=False, server_default=text("'0'"), comment='对应乐观锁的版本号')
    gmt_create = Column(DateTime, nullable=False, comment='对应记录的创建时间')
    gmt_modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='对应记录的修改时间')
    create_by = Column(String(250), nullable=False, comment='对应添加记录的人')
    modified_by = Column(String(250), nullable=False, comment='对应最后一次修改记录的')


class SysUser(Base):
    __tablename__ = 'sys_user'

    id = Column(BIGINT(20), primary_key=True, comment='主键')
    userid = Column(String(100))
    openid = Column(String(255))
    username = Column(VARCHAR(255))
    passwd = Column(String(255))
    phone = Column(String(255))
    nickname = Column(String(255))
    email = Column(String(50))
    avatar = Column(String(255), comment='用户头像')
    signature = Column(String(255), comment='签名')
    sex = Column(TINYINT(1), server_default=text("'0'"), comment='1-男性，2-女性，0-默认未知')
    address = Column(String(255), comment='联系地址')
    device_info = Column(String(1000))
    active = Column(TINYINT(1), server_default=text("'1'"))
    locked = Column(TINYINT(1), server_default=text("'0'"))
    version = Column(INTEGER(11), server_default=text("'0'"))
    gmt_create = Column(DateTime)
    gmt_modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_by = Column(String(255))
    create_by = Column(String(255))


class SysUserAddres(Base):
    __tablename__ = 'sys_user_address'

    id = Column(BIGINT(20), primary_key=True, comment='主键')
    userid = Column(String(255))
    name = Column(String(50))
    tel = Column(String(255))
    label = Column(String(255))
    value = Column(String(255))
    city_code = Column(String(255))
    detailed = Column(String(255))
    is_default = Column(TINYINT(1), server_default=text("'0'"))
    active = Column(TINYINT(1), nullable=False, server_default=text("'1'"), comment='对应该条记录是否可用，1可用，0不可用')
    version = Column(INTEGER(20), nullable=False, server_default=text("'0'"), comment='对应乐观锁的版本号')
    gmt_create = Column(DateTime, nullable=False, comment='对应记录的创建时间')
    gmt_modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='对应记录的修改时间')
    create_by = Column(String(250), nullable=False, comment='对应添加记录的人')
    modified_by = Column(String(250), nullable=False, comment='对应最后一次修改记录的')


class SysUserContact(Base):
    __tablename__ = 'sys_user_contact'

    id = Column(BIGINT(20), primary_key=True, comment='主键')
    userid = Column(String(255))
    name = Column(String(50))
    tel = Column(String(255))
    active = Column(TINYINT(1), nullable=False, server_default=text("'1'"), comment='对应该条记录是否可用，1可用，0不可用')
    version = Column(INTEGER(20), nullable=False, server_default=text("'0'"), comment='对应乐观锁的版本号')
    gmt_create = Column(DateTime, nullable=False, comment='对应记录的创建时间')
    gmt_modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='对应记录的修改时间')
    create_by = Column(String(250), nullable=False, comment='对应添加记录的人')
    modified_by = Column(String(250), nullable=False, comment='对应最后一次修改记录的')


class SysUserRole(Base):
    __tablename__ = 'sys_user_role'

    id = Column(BIGINT(20), primary_key=True)
    userid = Column(String(255))
    role_id = Column(BIGINT(20))
    active = Column(TINYINT(1), server_default=text("'1'"))
    version = Column(INTEGER(11), server_default=text("'0'"))
    gmt_create = Column(DateTime)
    gmt_modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    create_by = Column(String(255))
    modified_by = Column(String(255))
