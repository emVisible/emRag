from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

"""
  本文件为数据库初始化设置, 一般不会改动
"""
SQLAlchemy_DB = "sqlite:///./sql_app.db"

engine = create_engine(SQLAlchemy_DB, connect_args={"check_same_thread": False})

db_session_local = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    获取数据库实例
    """
    db = db_session_local()
    try:
        yield db
    finally:
        db.close()


def reset_db():
    # 删除所有表
    Base.metadata.drop_all(bind=engine)
    # 重新创建所有表
    Base.metadata.create_all(bind=engine)