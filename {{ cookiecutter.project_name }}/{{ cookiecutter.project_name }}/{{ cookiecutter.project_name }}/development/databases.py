{% if cookiecutter.without_mongo == "N" -%}
import mongoengine

MONGO_USER = 'root'
MONGO_PASS = 'mongoadmin'
MONGO_HOST = 'mongodb'
MONGO_DB_NAME = 'mongodb'
MONGO_DATABASE_HOST = f"mongodb://%s:%s@%s/%s" % (MONGO_USER, MONGO_PASS, MONGO_HOST, MONGO_DB_NAME)

mongoengine.connect(MONGO_DB_NAME, host=MONGO_DATABASE_HOST)
{%-endif %}
