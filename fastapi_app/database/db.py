from fastapi_app.database.models import *


try:
    db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
    db.generate_mapping(create_tables=True)
except Exception as ex:
    print(ex)
