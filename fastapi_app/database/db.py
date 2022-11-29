from .models import *


try:
    db.bind(provider='postgres',
            user='postgres',
            password='password',
            host='postgres',
            database='BTC_app_database')
    db.generate_mapping(create_tables=True)
except Exception as ex:
    print(ex)
