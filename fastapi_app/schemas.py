from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    id: int
    tg_id: str
    nickname: str = None
    create_date: datetime
    wallet: 'Wallet'
    sended_transactions: list['Transaction'] = None
    received_transactions: list['Transaction'] = None

    class Config:
        orm_mode = True


class Transaction(BaseModel):
    id: int
    sender: User = None
    receiver: User = None
    receiver_wallet: 'Wallet' = None
    sender_wallet: 'Wallet' = None
    sender_address: str
    receiver_address: str
    amount_btc_with_fee: float
    amount_btc_without_fee: float
    fee: float
    date_of_transaction: datetime
    tx_hash: str


class Wallet(BaseModel):
    id: int
    user: User
    balance: float
    private_key: str
    address: str
    received_transactions: list[Transaction] = []
    sended_transactions: list[Transaction] = []


class UserUpdate(BaseModel):
    id: int
    tg_id: str = None
    nickname: str = None
    create_date: datetime = None
    wallet: 'Wallet' = None


class UserCreate(BaseModel):
    tg_id: int
    nickname: str = None


class CreateTransaction(BaseModel):
    sender_id: int
    receiver_address: str
    amount_btc_without_fee: float
    fee: float = None
    testnet: bool = False


UserUpdate.update_forward_refs()


