# from database.models import *
from fastapi_app.database import crud
from fastapi_app import schemas
from fastapi import FastAPI, Body, Path

api = FastAPI()


@api.get("/users")
def get_all_users():
    """Информация по всем пользователям"""
    return {"all_users": crud.get_all_user()}


@api.get('/get_info_by_user/{user_id}')
def get_info_about_user(user_id: int = Path()):
    """Информация по пользователю по его id"""
    return {"user_info": crud.get_user_info(user_id)}


@api.get('/get_user_by_tg/{tg_id}')
def get_user_by_tg(tg_id: int):
    """Информация по пользователю по его tg_id"""
    user = crud.get_user_by_tg(tg_id)
    return {"user": user}


@api.post("/user/create")
def user_create(user: schemas.UserCreate = Body()):
    """Создание нового пользователя"""
    response = crud.create_user(tg_id=user.tg_id, nickname=user.nickname)
    return {"User created!": response.to_dict()}


@api.put("/user/{user_id}")
def update_user(user: schemas.UserUpdate = Body()):
    """
    Обновление информации по пользователю
    :param user
    """
    return {"updated_user": crud.update_user(user).to_dict()}


@api.delete('/user/{user_id}')
def delete_user(user_id: int = Path()):
    """
    Удалeние пользователя
    :param user_id:
    """
    crud.delete_user(user_id)
    return {"response": "User deleted"}


@api.get("/get_user_balance/{user_id}")
def user_balance_getter(user_id: int):
    """
    Получение баланса пользователя по его id
    :param user_id:
    """
    return {"user_balance": crud.get_user_balance(user_id)}


@api.get('/get_total_balance')
def get_total_balance():
    """
    Получение общего баланса всех кошельков
    """
    balance = crud.get_all_balance()
    return {"total_balance": balance}


@api.post("/create_transaction")
def create_transaction(trans_details: schemas.CreateTransaction):
    transaction = crud.create_transaction(
        sender_id=trans_details.sender_id,
        amount_btc_without_fee=trans_details.amount_btc_without_fee,
        receiver_address=trans_details.receiver_address,
        fee=trans_details.fee,
        testnet=trans_details.testnet
    )
    if isinstance(transaction, str):
        return {"error": transaction}
    return {"response": transaction.to_dict()}


# @api.get("/user/{user_id}")
# def read_user(user_id: str, query: str | None = None):
#     if query:
#         return {"item_id": user_id, "query": query}
#     return {"item_id": user_id}
