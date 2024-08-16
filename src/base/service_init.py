from sqlalchemy.orm import Session

from .auth.service_auth import hash_password
from .models import Role, User


def db_init(db: Session):
    db_role_init(db)
    db_user_init(db)
    db.commit()


def db_role_init(db: Session):
    roles = [
        Role(name="student"),
        Role(name="teacher"),
        Role(name="director"),
        Role(name="admin"),
        Role(name="root"),
    ]
    db.add_all(roles)


def db_user_init(db: Session):
    users = [
        User(
            name="root", email="root@qq.com", password=hash_password("root"), role_id=5
        ),
        User(
            name="admin",
            email="admin@qq.com",
            password=hash_password("admin"),
            role_id=4,
        ),
        User(
            name="director",
            email="director@qq.com",
            password=hash_password("director"),
            role_id=3,
        ),
        User(
            name="teacher",
            email="teacher@qq.com",
            password=hash_password("teacher"),
            role_id=2,
        ),
        User(
            name="student",
            email="student@qq.com",
            password=hash_password("student"),
            role_id=1,
        ),
    ]
    db.add_all(users)
