from fastapi_app.database.models import *


try:
    db.bind(provider='postgres',
            user='postgres',
            password='felts',
            host='localhost',
            database='BTC_app_database')
    db.generate_mapping(create_tables=True)
except Exception as ex:
    print(ex)
