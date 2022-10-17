from fastapi_app.database import users_crud, admins_crud
from fastapi_app.auth import get_current_user, authenticate_user, create_access_token
from fastapi_app import schemas
from fastapi.params import Depends
from pony.orm.core import ERDiagramError, TransactionIntegrityError
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import FastAPI, Body, Path, HTTPException, status, Response, Header
from fastapi_app.fastapi_config import SECRET_HEADER

api = FastAPI()


@api.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@api.get("/users/me/", response_model=schemas.Admin)
async def read_users_me(current_user: schemas.Admin = Depends(get_current_user)):
    return current_user


@api.get("/users")
def get_all_users(current_user: schemas.Admin = Depends(get_current_user)) -> dict:
    """Информация по всем пользователям"""
    try:
        all_users = admins_crud.get_all_user()
    except ERDiagramError as database_exception:
        return {"db_error": f'{database_exception}'}
    if all_users:
        return {"all_users": all_users}
    return {"not_found": "users not found in database"}


@api.get('/get_info_by_user/{user_id}')
def get_info_about_user(user_id: int = Path(), current_user: schemas.Admin = Depends(get_current_user)) -> dict:
    """Информация по пользователю по его id"""
    try:
        user_id = admins_crud.get_user_info(user_id)
    except ERDiagramError as database_exception:
        return {"db_error": f'{database_exception}'}
    if user_id:
        return {"user_info": user_id}
    return {"not_found": "user not found in database"}


@api.get('/get_user_by_tg/{tg_id}')
def get_user_by_tg(tg_id: int = Path(), secret_key: str = Header()) -> dict:
    """Информация по пользователю по его tg_id"""
    if secret_key == SECRET_HEADER:
        try:
            user = admins_crud.get_user_by_tg(tg_id)

        except ERDiagramError as database_exception:
            return {"db_error": f'{database_exception}'}

        if user:
            return {"user": user.to_dict()}
        return {"not_found": "user not found in database"}
    raise HTTPException(status_code=401)


@api.post("/user/create")
def user_create(user: schemas.UserCreate = Body(), secret_key: str = Header()) -> dict:
    """Создание нового пользователя"""
    if secret_key == SECRET_HEADER:
        try:
            new_user = users_crud.create_user(user)
        except ERDiagramError as database_exception:
            return {"db_error": f'{database_exception}'}
        except TransactionIntegrityError as database_error:
            return {"db_data_error": f'{database_error}'}
        return {"User_created!": new_user}
    raise HTTPException(status_code=401)


@api.put("/user/{user_id}")
def update_user(user: schemas.UserUpdate = Body(),
                current_user: schemas.Admin = Depends(get_current_user)) -> dict:
    """
    Обновление информации по пользователю
    :param user:
    :param current_user:
    """
    try:
        updated_user = admins_crud.update_user(user).to_dict()
    except ERDiagramError as database_exception:
        return {"db_error": f'{database_exception}'}
    return {"updated_user": updated_user}


@api.delete('/user/{user_id}')
def delete_user(user_id: int = Path(), current_user: schemas.Admin = Depends(get_current_user)) -> dict:
    """
    Удалeние пользователя
    :param user_id:
    :param current_user:
    """
    try:
        admins_crud.delete_user(user_id)
    except ERDiagramError as database_exception:
        return {"db_error": f'{database_exception}'}
    return {"successful": "User deleted"}


@api.get("/get_user_balance/{tg_id}")
def user_balance_getter(tg_id: int = Path(), secret_key: str = Header()) -> dict:
    """
    Получение баланса пользователя по его tg_id
    """
    if secret_key == SECRET_HEADER:
        try:
            user_balance = users_crud.get_user_balance(tg_id)
        except ERDiagramError as database_exception:
            return {"db_error": f'{database_exception}'}
        return {"balance": user_balance}
    raise HTTPException(status_code=401)


@api.get('/get_total_balance')
def get_total_balance(current_user: schemas.Admin = Depends(get_current_user)) -> dict:
    """
    Получение общего баланса всех кошельков
    """
    try:
        balance = admins_crud.get_all_balance()
    except ERDiagramError as database_exception:
        return {"db_error": f'{database_exception}'}
    return {"total_balance": balance}


@api.post("/create_transaction")
def create_transaction(trans_details: schemas.CreateTransaction, secret_key: str = Header()) -> dict:
    if secret_key == SECRET_HEADER:
        try:
            transaction = users_crud.create_transaction(
                sender_tg_id=trans_details.sender_tg_id,
                amount_btc_without_fee=trans_details.amount_btc_without_fee,
                receiver_address=trans_details.receiver_address,
                # fee=trans_details.fee,
                # testnet=trans_details.testnet
            )
        except ERDiagramError as database_exception:
            return {"db_error": f'{database_exception}'}
        if isinstance(transaction, str):
            return {"failed": transaction}
        return {"successful": transaction.to_dict()}
    raise HTTPException(status_code=401)


@api.get("/get_user_transactions/{tg_id}")
def get_transactions_by_tg(tg_id: int = Path(), secret_key: str = Header()):
    """Получение транзакций пользователя"""
    if secret_key == SECRET_HEADER:
        try:
            transactions = users_crud.get_user_transactions(tg_id=tg_id)
        except ERDiagramError as database_exception:
            return {"db_error": f'{database_exception}'}
        return {"transactions": transactions}
    raise HTTPException(status_code=401)

