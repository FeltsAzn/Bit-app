import uvicorn
from fastapi import FastAPI
from handlers import router


app = FastAPI(title='USERS', description='CRUD methods and logining for users', version='0.0.3')
app.include_router(router=router)

if __name__ == '__main__':
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
