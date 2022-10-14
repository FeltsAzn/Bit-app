from fastapi_app import schemas
import bit
from fastapi_app.database.db import *
from fastapi_app.database import admins_crud


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
        sender_tg_id: int,
        amount_btc_without_fee: float,
        receiver_address: str,
        fee: float | None,
        testnet: bool = False
) -> Transaction | str:
    """Возвращается информация по созданной транзакции, либо уведомление о недостаточном количество валюты"""
    sender = admins_crud.get_user_by_tg(sender_tg_id)
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
def get_user_balance(tg_id: int) -> float:
    """Возвращается число с плавающей точкой (для пользователей)"""
    user = admins_crud.get_user_by_tg(tg_id)
    user_wallet = admins_crud.update_wallet_balance(user.wallet)
    return user_wallet.balance


@db_session
def get_transaction_info(transaction: schemas.Transaction) -> dict:
    """Возвращается словарь с информацией по транзакции (для пользователей)"""
    return {"id": transaction.id,
            "sender": transaction.sender if transaction.sender else None,
            "receiver": transaction.receiver if transaction.receiver else None,
            "sender_wallet": transaction.sender_wallet if transaction.sender_wallet else None,
            "receiver_wallet": transaction.receiver_wallet if transaction.receiver_wallet else None,
            "sender_address": transaction.sender_address,
            "receiver_address": transaction.receiver_address,
            "amount_btc_with_fee": transaction.amount_btc_with_fee,
            "amount_btc_without_fee": transaction.amount_btc_without_fee,
            "fee": transaction.fee,
            "date_of_transaction": transaction.date_of_transaction,
            "tx_hash": transaction.tx_hash}


@db_session
def get_user_transactions(tg_id: int) -> list[dict]:
    user = admins_crud.get_user_by_tg(tg_id)
    transactions = []
    for transaction in Transaction.select(lambda tr: user == tr.sender)[:]:
        transactions.append(transaction.to_dict())
    return transactions

