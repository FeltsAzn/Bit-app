from fastapi_app import schemas
import bit
from fastapi_app.database.db import *


@db_session
def create_wallet(user: schemas.User = None, private_key: str = None, testnet: bool = False) -> Wallet:
    """Возвращается экземпляр pony.orm.Wallet для передачи новому пользователю"""
    if testnet:
        raw_wallet = bit.PrivateKeyTestnet() if private_key is None else bit.PrivateKeyTestnet(private_key)
    else:
        raw_wallet = bit.Key() if private_key is None else bit.Key(private_key)
    if user is None:
        wallet = Wallet(private_key=raw_wallet.to_wif(), address=raw_wallet.address)
    else:
        wallet = Wallet(user=user, private_key=raw_wallet.to_wif(), address=raw_wallet.address)
    flush()
    return wallet


@db_session
def create_user(user: schemas.UserCreate) -> User:
    """Возвращается информация в виде словаря по созданному пользователю"""
    tg_id: int = user.tg_id
    nickname: str | None = user.nickname
    if nickname is None:
        user = User(tg_id=tg_id, wallet=create_wallet())
    else:
        user = User(tg_id=tg_id, nickname=nickname, wallet=create_wallet())
    return user.to_dict()


@db_session
def create_transaction(
        sender_id: int,
        amount_btc_without_fee: float,
        receiver_address: str,
        fee: float | None,
        testnet: bool = False
) -> Transaction | str:
    """Возвращается информация по созданной транзакции, либо уведомление о недостаточном количество валюты"""
    sender = get_user(sender_id)
    wallet_sender = bit.PrivateKeyTestnet(sender.wallet.private_key) if testnet else bit.Key(sender.wallet.private_key)
    sender.wallet.balance = wallet_sender.get_balance()
    if fee is None:
        fee = bit.network.fees.get_fee() * 1000
    amount_btc_with_fee = amount_btc_without_fee + fee
    if amount_btc_with_fee >= sender.wallet.balance:
        return f'Too low balance {sender.wallet.balance}'

    output = [(receiver_address, amount_btc_without_fee, 'satoshi')]

    tx_hash = wallet_sender.send(output, fee, absolute_fee=True)

    transaction = Transaction(
        sender=sender,
        sender_wallet=sender.wallet,
        fee=fee,
        sender_address=sender.wallet.address,
        receiver_address=receiver_address,
        amount_btc_with_fee=amount_btc_with_fee,
        amount_btc_without_fee=amount_btc_without_fee,
        tx_hash=tx_hash
    )
    return transaction.to_dict()


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
    """Возвращается общий баланс всех пользователей"""
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
def get_user_balance(user_id: int) -> float:
    """Возвращается число с плавающей точкой (для пользователей)"""
    user_wallet = update_wallet_balance(User[user_id].wallet)
    return user_wallet.balance


@db_session
def get_wallet_info(wallet: schemas.Wallet) -> dict:
    """Возвращается словарь с информацией по кошельку для передачи в информацию по пользователю"""
    wallet = update_wallet_balance(wallet)
    return {"id": wallet.id if wallet.id else None,
            "user": wallet.user if wallet.user else None,
            "balance": wallet.balance if wallet.balance else None,
            "private_key": wallet.private_key if wallet.private_key else None,
            "address": wallet.address if wallet.address else None,
            "sended_transactions": wallet.sended_transactions if wallet.sended_transactions else [],
            "received_transactions": wallet.received_transactions if wallet.received_transactions else []}


@db_session
def get_user_info(user_id: int) -> dict:
    """Возвращается словарь с информацией о пользователе (для админов)"""
    user = get_user(user_id)
    return {"id": user.id,
            "tg_id": user.tg_id,
            "nick": user.nickname if user.nickname else None,
            "create_date": user.create_date,
            # получаем все данные по кошельку
            "wallet": get_wallet_info(user.wallet),
            "sended_transactions": user.sended_transactions if user.sended_transactions else [],
            "received_transactions": user.received_transactions if user.received_transactions else []}


@db_session
def delete_user(user_id: int) -> bool:
    """Удаление пользователя по его id в БД (для админов)"""
    User[user_id].delete()
    return True
