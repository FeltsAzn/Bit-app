from http.client import HTTPException
from tg_bot.config import API_URL
import requests
from fastapi_app import schemas


def get_users():
    """
    Получаем всех юзеров
    :return list:
    """
    try:
        response = requests.get(f"{API_URL}/users").json()
    except requests.exceptions.ConnectionError  as _ex:
        raise _ex
    return response


def get_info_about_user(user_id: int):
    try:
        response = requests.get(f'{API_URL}/get_info_by_user/{user_id}').json()
    except requests.exceptions.ConnectionError as _ex:
        return {"server_error": "the server is not responding"}
    return response


def get_user_by_tg(tg_id: int):
    try:
        response = requests.get(f'{API_URL}/get_user_by_tg/{tg_id}').json()
    except requests.exceptions.ConnectionError as _ex:
        return {"server_error": "the server is not responding"}
    return response


def create_user(user: dict):
    """
    Создаем Юзера
    :param user:
    :return:
    """
    user = schemas.UserCreate.validate(user)
    try:
        response = requests.post(f'{API_URL}/user/create', data=user.json())
    except requests.exceptions.ConnectionError as _ex:
        return {"server_error": "the server is not responding"}
    return response


def create_transaction(transaction_info: schemas.CreateTransaction) -> dict:
    try:
        transaction_info = schemas.CreateTransaction.validate(transaction_info)
        response = requests.post(f'{API_URL}/create_transaction', data=transaction_info.json()).json()
    except requests.exceptions.ConnectionError as _ex:
        return {"server_error": "the server is not responding"}
    return response


def update_user(user: schemas.UserUpdate) -> str | dict:
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
    try:
        response = requests.delete(f'{API_URL}/user/{user_id}').json()
    except requests.exceptions.ConnectionError as _ex:
        return {"server_error": "the server is not responding"}
    return response


def get_user_balance(tg_id: int) -> dict:
    try:
        response = requests.get(f"{API_URL}/get_user_balance/{tg_id}").json()
    except requests.exceptions.ConnectionError as _ex:
        return {"server_error": "the server is not responding"}
    return response


def total_balance() -> dict:
    try:
        response = requests.get(f"{API_URL}/get_total_balance").json()
    except requests.exceptions.ConnectionError as _ex:
        return {"server_error": "the server is not responding"}
    return response


def get_user_transactions(tg_id: int):
    try:
        response = requests.get(f"{API_URL}/get_user_transactions/{tg_id}").json()
    except requests.exceptions.ConnectionError as _ex:
        return {"server_error": "the server is not responding"}
    return response
