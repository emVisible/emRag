from langchain.docstore.document import Document
from src.vector_store.service import tenant_create, database_create, collection_create
from src.base.models import Tenant, Database, Collection
from sqlalchemy.orm import Session


async def init_vector_db(db: Session):
    await db_tenants_init(db)
    await database_init(db)
    await collections_init(db)


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
        tenant_create(name=name)
        db.add(Tenant(name=name))
    db.commit()


async def database_init(db: Session):
    databases = [
        Database(name="public", tenant_name="School of Asian Languages and Cultures"),
        Database(name="private", tenant_name="School of Asian Languages and Cultures"),
        Database(
            name="public",
            tenant_name="School of Education",
        ),
        Database(
            name="private",
            tenant_name="School of Education",
        ),
    ]
    for database in databases:
        database_create(name=database.name, tenant=database.tenant_name)
        db.add(database)
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
    collections = [
        Collection(name="edu_c_1", database_id=database_id),
        Collection(name="edu_c_2", database_id=database_id),
    ]
    for collection in collections:
        database = (
            db.query(Database).filter(Database.id == collection.database_id).first()
        )
        describe = {
            "collection_name": collection.name,
            "database_name": database.name,
            "tenant_name": database.tenant_name,
        }
        collection_create(
            name=collection.name,
            tenant_name=database.tenant_name,
            database_name=database.name,
            metadata=describe,
        )
        db.add(collection)
    db.commit()
