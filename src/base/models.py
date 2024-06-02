from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

"""
  该文件为数据库中的表信息, 即SQLite表信息
"""


class User(Base):
    """
    用户类, 表名为users
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String, unique=True, index=True)
    password = Column(String)
    history = relationship("History", back_populates="owner")


class History(Base):
    """
    历史记录类, 表名为history, 通过外键约束绑定多个历史记录到一个用户上
    """

    __tablename__ = "history"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)

    owner = relationship("User", back_populates="history")
    owner_id = Column(Integer, ForeignKey("users.id"))
