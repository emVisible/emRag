from src.vector_store.service import tenant_create


def init_vector_db():
  init_tenant()
  init_database()


def init_tenant():
    colleges = [
        "School of English Studies",
        "School of Asian Languages and Cultures",
        "School of European Languages and Cultures",
        "School of Chinese Studies",
        "School of International Business, School of Innovation and Entrepreneurship",
        "School of Education",
        "School of Culture and Tourism",
        "School of Arts",
    ]
    for college in colleges:
        tenant_create(name=college)
    return "OK"


def init_database():
    pass