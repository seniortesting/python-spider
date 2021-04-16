# coding: utf-8
from sqlalchemy import Column, DateTime, String, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class ProxyRaw(Base):
    __tablename__ = 'proxy_raw'

    id = Column(BIGINT(20), primary_key=True)
    name = Column(String(50))
    proxy = Column(String(255))
    https = Column(TINYINT(1), server_default=text("'0'"))
    proxy_type = Column(String(255),server_default=text(""))
    china = Column(String(255),server_default=text(""))
    location = Column(String(255),server_default=text(""))
    success = Column(INTEGER(11),server_default=text("'0'"))
    fail = Column(INTEGER(11),server_default=text("'0'"))
    total = Column(INTEGER(11),server_default=text("'0'"))
    quality = Column(INTEGER(11),server_default=text("'0'"))
    last_status = Column(TINYINT(1),server_default=text("'0'"))
    gmt_create = Column(DateTime)
    gmt_modified = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    def serialize(self):
        return {
            'name':self.name,
            'proxy':self.proxy,
            'success':self.success,
            'fail':self.fail,
            'total': self.total,
            'quality':self.quality,
            'last_status': self.last_status,
            'last_time': self.gmt_modified
        }


class ProxyValid(Base):
    __tablename__ = 'proxy_valid'

    id = Column(BIGINT(20), primary_key=True)
    name = Column(String(50))
    proxy = Column(String(255))
    https = Column(TINYINT(1), server_default=text("'0'"))
    proxy_type = Column(String(255),server_default=text(""))
    china = Column(String(255),server_default=text(""))
    location = Column(String(255),server_default=text(""))
    success = Column(INTEGER(11),server_default=text("'0'"))
    fail = Column(INTEGER(11),server_default=text("'0'"))
    total = Column(INTEGER(11),server_default=text("'0'"))
    quality = Column(INTEGER(11),server_default=text("'0'"))
    last_status = Column(TINYINT(1),server_default=text("'0'"))
    gmt_create = Column(DateTime)
    gmt_modified = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    def serialize(self):
        return {
            'name':self.name,
            'proxy':self.proxy,
            'success':self.success,
            'fail':self.fail,
            'total': self.total,
            'quality':self.quality,
            'last_status': self.last_status,
            'last_time': self.gmt_modified
        }
