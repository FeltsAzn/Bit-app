from pydantic import BaseModel


class UserUpdate(BaseModel):
    id: int
    tg_id: str = None
    nickname: str = None


class UserCreate(BaseModel):
    tg_id: int
    nickname: str = None
    is_admin: bool = False


class CreateTransaction(BaseModel):
    sender_tg_id: int
    receiver_address: str
    amount_btc_without_fee: float
    # fee: float = None
    # testnet: bool = False



