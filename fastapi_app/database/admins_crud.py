from fastapi_app import schemas
import bit
from .db import *


@db_session
def update_user(user: schemas.UserUpdate) -> User:
    """Возвращается информация об обновленном пользователе в виде словаря"""
    user_to_update = User[user.id]
    if user.tg_id:
        user_to_update.tg_id = user.tg_id
    if user.nickname:
        user_to_update.nickname = user.nickname
    if user.create_date:
        user_to_update.create_date = user.create_date
    if user.wallet:
        user_to_update.wallet = user.wallet
    return user_to_update.to_dict()


@db_session
def update_wallet_balance(wallet: schemas.Wallet) -> Wallet:
    """Возвращается экземпляр pony.orm.Wallet"""
    testnet = True if wallet.private_key.startswith('c') else False
    # получаем объект из Bit, для работы с биткоинами
    bit_wallet = bit.Key(wallet.private_key) if not testnet else bit.PrivateKeyTestnet(wallet.private_key)
    # получаем баланс кошелька и присваиваем значение кошельку в нашей бд
    wallet.balance = bit_wallet.get_balance()
    return wallet


@db_session
def get_all_balance() -> float:
    """Возвращается общий баланс всех пользователей (для админов)"""
    all_balance = 0
    # с помощью генераторного выражения выбираем все кошельки, с помощью функции select()
    for wallet in select(w for w in Wallet)[:]:
        update_wallet_balance(wallet)
        all_balance += wallet.balance
    return all_balance


@db_session
def get_user(user_id: int) -> User:
    """Возвращается экземпляр pony.orm.User"""
    return User[user_id]


@db_session
def get_user_by_tg(tg_id: int) -> User:
    """Возвращается экземпляр pony.orm.User"""
    return User.select(lambda u: u.tg_id == tg_id).first()


@db_session
def get_all_user() -> list[dict]:
    """Возвращается список всех пользователей в виде словаря (для админов)"""
    all_users = []
    for user in User.select()[:]:
        all_users.append(user.to_dict())
    return all_users


@db_session
def get_wallet_info(wallet: schemas.Wallet) -> dict:
    """Возвращается словарь с информацией по кошельку для передачи в информацию по пользователю"""
    wallet = update_wallet_balance(wallet)
    return {"id": wallet.id,
            "user": wallet.user if wallet.user else None,
            "balance": wallet.balance,
            "private_key": wallet.private_key,
            "address": wallet.address,
            "sended_transactions": wallet.sended_transactions if wallet.sended_transactions else [],
            "received_transactions": wallet.received_transactions if wallet.received_transactions else []}


@db_session
def get_user_info(user_id: int) -> dict:
    """Возвращается словарь с информацией о пользователе (для админов)"""
    user = get_user(user_id)
    return {"id": user.id,
            "tg_id": user.tg_id,
            "nickname": user.nickname if user.nickname else None,
            "create_date": user.create_date,
            "is_admin": user.is_admin,
            # получаем все данные по кошельку
            "wallet": get_wallet_info(user.wallet)}


@db_session
def delete_user(user_id: int) -> bool:
    """Удаление пользователя по его id в БД (для админов)"""
    User[user_id].delete()
    return True
