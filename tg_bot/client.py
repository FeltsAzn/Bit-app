from tg_bot.config import API_URL
import requests
from fastapi_app import schemas


def get_users():
    """
    Получаем всех юзеров
    :return list:
    """
    return requests.get(f"{API_URL}/users").json()


def get_info_about_user(user_id: int):
    return requests.get(f'{API_URL}/get_info_by_user/{user_id}').json()


def get_user_by_tg(tg_id: int):
    return requests.get(f'{API_URL}/get_user_by_tg/{tg_id}').json()


def create_user(user: schemas.UserCreate):
    """
    Создаем Юзера
    :param user:
    :return:
    """
    user = schemas.UserCreate.validate(user)
    return requests.post(f'{API_URL}/user/create', data=user.json()).json()


def create_transaction(transaction_info: schemas.CreateTransaction):
    transaction_info = schemas.CreateTransaction.validate(transaction_info)
    return requests.post(f'{API_URL}/create_transaction', data=transaction_info.json()).json()


def update_user(user: schemas.UserUpdate):
    user = schemas.UserUpdate.validate(user)
    response = requests.put(f'{API_URL}/user/{user.id}', data=user.json())
    try:
        return response.json()
    except Exception as ex:
        return response.text


def delete_user(user_id: int):
    return requests.delete(f'{API_URL}/user/{user_id}').json()


def get_user_balance(user_id: int):
    return requests.get(f"{API_URL}/get_user_balance/{user_id}").json()


def total_balance():
    return requests.get(f"{API_URL}/get_total_balance").json()

def g

