from .models import *


db.bind(provider='postgres',
        user='postgres',
        password='felts',
        host='db_postgres',
        port='5432',
        database='BTC_app_database')
db.generate_mapping(create_tables=True)
