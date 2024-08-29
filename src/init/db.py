from sqlalchemy.orm import Session
from src.base.auth.service_auth import hash_password
from src.base.models import Role, User, Tenant, Database, Collection
from time import sleep


async def db_init(db: Session):
    await db_role_init(db)
    await db_user_init(db)
    await db_tenants_init(db)
    await database_init(db)
    await collections_init(db)


async def db_role_init(db: Session):
    roles = [
        Role(name="student"),
        Role(name="teacher"),
        Role(name="director"),
        Role(name="admin"),
        Role(name="root"),
    ]
    db.add_all(roles)
    db.commit()


async def db_user_init(db: Session):
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
    db.commit()


async def db_tenants_init(db: Session):
    names = [
        "School of Asian Languages and Cultures",
        "School of European Languages and Cultures",
        "School of Chinese Studies",
        "School of International Business, School of Innovation and Entrepreneurship",
        "School of Education",
        "School of Culture and Tourism",
        "School of Arts",
    ]
    for name in names:
        db.add(Tenant(name=name))
    db.commit()


async def database_init(db: Session):
    asian_languages_and_cultrues = Database(
        name="public", tenant_name="School of Asian Languages and Cultures"
    )
    asian_languages_and_cultrues_private = Database(
        name="private", tenant_name="School of Asian Languages and Cultures"
    )
    education = Database(
        name="public",
        tenant_name="School of Education",
    )
    education_private = Database(
        name="private",
        tenant_name="School of Education",
    )
    db.add_all(
        [
            asian_languages_and_cultrues,
            asian_languages_and_cultrues_private,
            education,
            education_private,
        ]
    )
    db.commit()


async def collections_init(db: Session):
    database_id = (
        db.query(Database)
        .filter(
            Database.tenant_name == "School of Education" and Database.name == "public"
        )
        .first()
        .id
    )
    education_public_collection1 = Collection(name="edu_c_1", database_id=database_id)
    db.add_all([education_public_collection1])
    db.commit()
