# from database.models import *
from pony.orm.core import ERDiagramError, TransactionIntegrityError

from fastapi_app.database import users_crud, admins_crud
from fastapi_app import schemas
from fastapi import FastAPI, Body, Path

api = FastAPI()


@api.get("/users")
def get_all_users() -> dict:
    """Информация по всем пользователям"""
    try:
        all_users = admins_crud.get_all_user()
    except ERDiagramError as database_exception:
        return {"db_error": f'{database_exception}'}
    if all_users:
        return {"all_users": all_users}
    return {"not_found": "users not found in database"}


@api.get('/get_info_by_user/{user_id}')
def get_info_about_user(user_id: int = Path()) -> dict:
    """Информация по пользователю по его id"""
    try:
        user_id = admins_crud.get_user_info(user_id)
    except ERDiagramError as database_exception:
        return {"db_error": f'{database_exception}'}
    if user_id:
        return {"user_info": user_id}
    return {"not_found": "user not found in database"}


@api.get('/get_user_by_tg/{tg_id}')
def get_user_by_tg(tg_id: int) -> dict:
    """Информация по пользователю по его tg_id"""
    try:
        user = admins_crud.get_user_by_tg(tg_id)

    except ERDiagramError as database_exception:
        return {"db_error": f'{database_exception}'}

    if user:
        return {"user": user.to_dict()}
    return {"not_found": "user not found in database"}


@api.post("/user/create")
def user_create(user: schemas.UserCreate = Body()) -> dict:
    """Создание нового пользователя"""
    try:
        new_user = users_crud.create_user(user)
    except ERDiagramError as database_exception:
        return {"db_error": f'{database_exception}'}
    except TransactionIntegrityError as database_error:
        return {"db_data_error": f'{database_error}'}
    return {"User_created!": new_user}


@api.put("/user/{user_id}")
def update_user(user: schemas.UserUpdate = Body()) -> dict:
    """
    Обновление информации по пользователю
    :param user
    """
    try:
        updated_user = admins_crud.update_user(user).to_dict()
    except ERDiagramError as database_exception:
        return {"db_error": f'{database_exception}'}
    return {"updated_user": updated_user}


@api.delete('/user/{user_id}')
def delete_user(user_id: int = Path()) -> dict:
    """
    Удалeние пользователя
    :param user_id:
    """
    try:
        admins_crud.delete_user(user_id)
    except ERDiagramError as database_exception:
        return {"db_error": f'{database_exception}'}
    return {"successful": "User deleted"}


@api.get("/get_user_balance/{tg_id}")
def user_balance_getter(tg_id: int = Path()) -> dict:
    """
    Получение баланса пользователя по его tg_id
    :param tg_id:
    """
    try:
        user_balance = users_crud.get_user_balance(tg_id)
    except ERDiagramError as database_exception:
        return {"db_error": f'{database_exception}'}
    return {"balance": user_balance}


@api.get('/get_total_balance')
def get_total_balance() -> dict:
    """
    Получение общего баланса всех кошельков
    """
    try:
        balance = admins_crud.get_all_balance()
    except ERDiagramError as database_exception:
        return {"db_error": f'{database_exception}'}
    return {"total_balance": balance}


@api.post("/create_transaction")
def create_transaction(trans_details: schemas.CreateTransaction) -> dict:
    try:
        transaction = users_crud.create_transaction(
            sender_id=trans_details.sender_tg_id,
            amount_btc_without_fee=trans_details.amount_btc_without_fee,
            receiver_address=trans_details.receiver_address,
            fee=trans_details.fee,
            testnet=trans_details.testnet
        )
    except ERDiagramError as database_exception:
        return {"db_error": f'{database_exception}'}
    if isinstance(transaction, str):
        return {"failed": transaction}
    return {"successful": transaction.to_dict()}


@api.get("/get_user_transactions/{tg_id}")
def get_transactions_by_tg(tg_id: int = Path()):
    """Получение транзакций пользователя"""
    try:
        transactions = users_crud.get_user_transactions(tg_id=tg_id)
    except ERDiagramError as database_exception:
        return {"db_error": f'{database_exception}'}
    return {"transactions": transactions}



# @api.get("/user/{user_id}")
# def read_user(user_id: str, query: str | None = None):
#     if query:
#         return {"item_id": user_id, "query": query}
#     return {"item_id": user_id}
