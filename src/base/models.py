from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

"""
  该文件为数据库中的表信息, 即SQLite表信息
"""


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    members = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    role = relationship("Role", back_populates="members")
    role_id = Column(Integer, ForeignKey("roles.id"))


# 与向量数据库同步更新


class Tenant(Base):
    __tablename__ = "tenants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    databases = relationship("Database", back_populates="tenant")


class Database(Base):
    __tablename__ = "databases"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    tenant = relationship("Tenant", back_populates="databases")
    tenant_name = Column(Integer, ForeignKey("tenants.name"))
    collections = relationship("Collection", back_populates="database")


class Collection(Base):
    __tablename__ = "collections"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    database = relationship("Database", back_populates="collections")
    database_id = Column(Integer, ForeignKey("databases.id"))
