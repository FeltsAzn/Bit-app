from tg_bot.tg_bot_config import API_URL, SECRET_HEADER
import requests
from fastapi_app import schemas

users_token_cache = {}


def get_users():
    """
    Получаем всех юзеров (для админов)
    :return server response(list):
    """
    try:
        response = requests.get(f"{API_URL}/users").json()
    except requests.exceptions.ConnectionError as _ex:
        raise _ex
    return response


def get_info_about_user(user_id: int):
    """
    Получение информации о пользователе (для админа)
    :param user_id:
    :return server response(dict):
    """
    try:
        response = requests.get(f'{API_URL}/get_info_by_user/{user_id}').json()
    except requests.exceptions.ConnectionError as _ex:
        return {"server_error": "the server is not responding"}
    return response


def get_user_by_tg(tg_id: int):
    """
    Получение информации о пользователе
    :param tg_id:
    :return server response(dict):
    """
    try:
        response = requests.get(f'{API_URL}/get_user_by_tg/{tg_id}',
                                headers={"secret-key": SECRET_HEADER}).json()
    except requests.exceptions.ConnectionError as _ex:
        return {"server_error": "the server is not responding"}
    return response


def create_user(user: dict):
    """
    Создание пользователя
    :param user:
    :return server response(dict):
    """
    user = schemas.UserCreate.validate(user)
    try:
        response = requests.post(f'{API_URL}/user/create',
                                 data=user.json(),
                                 headers={"secret-key": SECRET_HEADER}).json()
    except requests.exceptions.ConnectionError as _ex:
        return {"server_error": "the server is not responding"}
    return response


def update_user(user: schemas.UserUpdate) -> str | dict:
    """
    Обновление информации пользователя (для админа)
    :param user:
    :return server response(dict | str) :
    """
    try:
        user = schemas.UserUpdate.validate(user)
        response = requests.put(f'{API_URL}/user/{user.id}', data=user.json())
    except requests.exceptions.ConnectionError as _ex:
        return {"server_error": "the server is not responding"}
    else:
        try:
            return response.json()
        except Exception as ex:
            return response.text


def delete_user(user_id: int) -> dict:
    """
    Удаление пользователя (для админа)
    :param user_id:
    :return server response(dict):
    """
    try:
        response = requests.delete(f'{API_URL}/user/{user_id}').json()
    except requests.exceptions.ConnectionError as _ex:
        return {"server_error": "the server is not responding"}
    return response


def get_user_balance(tg_id: int) -> dict:
    """
    Получение баланса пользователя
    :param tg_id:
    :return server response(dict):
    """
    try:
        response = requests.get(f"{API_URL}/get_user_balance/{tg_id}",
                                headers={"secret-key": SECRET_HEADER}).json()
    except requests.exceptions.ConnectionError as _ex:
        return {"server_error": "the server is not responding"}
    return response


def total_balance() -> dict:
    """
    Получение общего баланса пользователей (для админа)
    :return server response(dict):
    """
    try:
        response = requests.get(f"{API_URL}/get_total_balance").json()
    except requests.exceptions.ConnectionError as _ex:
        return {"server_error": "the server is not responding"}
    return response


def create_transaction(transaction_info: dict) -> dict:
    """
    Создание транзакции
    :param transaction_info:
    :return server response(dict):
    """
    try:
        transaction_info = schemas.CreateTransaction.validate(transaction_info)
        response = requests.post(f'{API_URL}/create_transaction',
                                 data=transaction_info.json(),
                                 headers={"secret-key": SECRET_HEADER}).json()
    except requests.exceptions.ConnectionError as _ex:
        return {"server_error": "the server is not responding"}
    return response


def get_user_transactions(tg_id: int) -> dict:
    """
    Получение общего баланса пользователей
    :param tg_id:
    :return server response(dict):
    """
    try:
        response = requests.get(f"{API_URL}/get_user_transactions/{tg_id}",
                                headers={"secret-key": SECRET_HEADER}).json()
    except requests.exceptions.ConnectionError as _ex:
        return {"server_error": "the server is not responding"}
    return response
