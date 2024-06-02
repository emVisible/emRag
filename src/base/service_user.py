from sqlalchemy.orm import Session
from passlib.context import CryptContext
from . import models, schemas



def get_user(db: Session, user_id: int):
    """
    从数据库中, 根据user_id, 获取唯一用户
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_name(db: Session, username: str):
    """
    从数据库中, 根据name, 获取唯一用户
    """
    return db.query(models.User).filter(models.User.name == username).first()


def get_user_by_email(db: Session, user_email: str):
    """
    从数据库中, 根据user_email, 获取唯一用户
    """
    return db.query(models.User).filter(models.User.email == user_email).first()


def get_users(db: Session, offset: int | None, limit: int | None):
    """
    从数据库中获取所有用户
    offset: 查询偏移, 每隔offset输出一次
    limit:  最大获取用户数量
    """
    return db.query(models.User).offset(offset=offset).limit(limit=limit).all()


def get_history_all(db: Session, limit: int | None):
    """
    从数据库中获取所有历史记录
    limit: 最大获取历史记录数量
    """
    return db.query(models.History).limit(limit=limit).all()




def create_history(db: Session, history: schemas.History, user_id: int):
    """
    创建历史记录, 将历史记录绑定到对应用户id上
    content:  具体的历史记录内容
    owner_id: 用户id
    """
    new_history = models.History(content=history.content, owner_id=user_id)
    db.add(new_history)
    db.commit()
    db.refresh(new_history)
    return new_history
