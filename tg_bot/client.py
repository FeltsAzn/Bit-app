from tg_bot_config import API_URL, SECRET_HEADER, ADMIN_PASSWORD, ADMIN_ID
import requests
import tg_schemas


def request():
    form_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = f'username={ADMIN_ID[0]}&password={ADMIN_PASSWORD}'
    raw_token = requests.post(API_URL + "/token",
                              headers=form_headers,
                              data=payload)
    token = raw_token.json()
    admin_session = requests.Session()
    admin_session.headers = {
        'accept': 'application/json',
        'Authorization': "Bearer " + token['access_token']
    }
    user_session = requests.Session()
    user_session.headers = {
        "secret-key": SECRET_HEADER
    }
    return user_session, admin_session


user_session, admin_session = request()


def get_user_by_tg(tg_id: int):
    """
    Получение информации о пользователе
    :param tg_id:
    :return server response(dict):
    """
    try:
        response = user_session.get(f'{API_URL}/get_user_by_tg/{tg_id}').json()
    except requests.exceptions.ConnectionError as _ex:
        return {"server_error": "the server is not responding"}
    return response


def create_user(user: dict):
    """
    Создание пользователя
    :param user:
    :return server response(dict):
    """
    user = tg_schemas.UserCreate.validate(user)
    try:
        response = user_session.post(f'{API_URL}/user/create',
                                     data=user.json()).json()
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
        transaction_info = tg_schemas.CreateTransaction.validate(transaction_info)
        response = user_session.post(f'{API_URL}/create_transaction',
                                     data=transaction_info.json()).json()
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
        response = user_session.get(f"{API_URL}/get_user_transactions/{tg_id}").json()
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
        response = user_session.get(f"{API_URL}/get_user_balance/{tg_id}").json()
    except requests.exceptions.ConnectionError as _ex:
        return {"server_error": "the server is not responding"}
    return response


def get_users():
    """
    Получаем всех юзеров (для админов)
    :return server response(list):
    """
    try:
        response = admin_session.get(f"{API_URL}/users").json()
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
        response = admin_session.get(f'{API_URL}/get_info_by_user/{user_id}').json()
    except requests.exceptions.ConnectionError as _ex:
        return {"server_error": "the server is not responding"}
    return response


def update_user(user: tg_schemas.UserUpdate) -> str | dict:
    """
    Обновление информации пользователя (для админа)
    :param user:
    :return server response(dict | str) :
    """
    try:
        user = tg_schemas.UserUpdate.validate(user)
        response = admin_session.put(f'{API_URL}/user/{user.id}', data=user.json())
    except requests.exceptions.ConnectionError as _ex:
        return {"server_error": "the server is not responding"}
    else:
        try:
            return response.json()
        except Exception:
            return response.text


def delete_user(user_id: int) -> dict:
    """
    Удаление пользователя (для админа)
    :param user_id:
    :return server response(dict):
    """
    try:
        response = admin_session.delete(f'{API_URL}/user/{user_id}').json()
    except requests.exceptions.ConnectionError as _ex:
        return {"server_error": "the server is not responding"}
    return response


def total_balance() -> dict:
    """
    Получение общего баланса пользователей (для админа)
    :return server response(dict):
    """
    try:
        response = admin_session.get(f"{API_URL}/get_total_balance").json()
    except requests.exceptions.ConnectionError as _ex:
        return {"server_error": "the server is not responding"}
    return response
