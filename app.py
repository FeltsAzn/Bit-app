# from database.models import *
from database import crud
import pydantic_models
import config
from fastapi import FastAPI, Query, Body, Path

api = FastAPI()


@api.get('/get_info_by_user/{user_id}')
def get_info_about_user(user_id: int):
    return crud.get_user_info(user_id)


@api.post("/user/create")
def user_create(user: pydantic_models.UserCreate = Body()) -> dict:
    response = crud.create_user(tg_id=user.tg_id, nickname=user.nickname)
    return {"User created!": response.to_dict()}


@api.put("/user/{user_id}")
def update_user(user_id: int, user: pydantic_models.UserUpdate = Body()) -> pydantic_models.User:
    return crud.update_user(user).to_dict()


@api.delete('/user/{user_id}')
def delete_user(user_id: int = Path()) -> dict:
    crud.delete_user(user_id)
    return {"response": "User deleted"}


#
#
# @api.get("/users/")
# def users_getter(skip: int = 0, limit: int = 10):
#     return fake_database["users"][skip: skip + limit]
#
#
# @api.get("/get_user_balance/{user_id}")
# def user_balance_getter(user_id: int):
#     return fake_database['users'][user_id - 1]['balance']
#
# @api.get("/all_balance")
# def all_balance_getter():
#     total_balance: float = 0.0
#     for user in fake_database["users"]:
#         total_balance += pydantic_models.User(**user).balance
#     return total_balance

@api.get("/user/{user_id}")
def read_user(user_id: str, query: str | None = None):
    if query:
        return {"item_id": user_id, "query": query}
    return {"item_id": user_id}
