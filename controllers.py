from fastapi import APIRouter

from repositories import AccountRepository, TransactionRepository, UserRepository
from schemas import (AccountCreate, AccountResponse, AmountRequest,
                     TransactionResponse, UserCreate, UserResponse)
from services import AccountService, UserService

# Wiring: create repositories and give them to the services
user_repo = UserRepository()
account_repo = AccountRepository()
txn_repo = TransactionRepository()
user_service = UserService(user_repo)
account_service = AccountService(user_repo, account_repo, txn_repo)

router = APIRouter(prefix="/api")


def to_account_response(account) -> AccountResponse:
    user = user_service.get_user(account.user_id)
    return AccountResponse(
        accountId=account.account_id,
        userName=user.name,
        accountType=account.account_type,
        balance=float(account.balance),
    )


@router.post("/users", response_model=UserResponse, status_code=201)
def create_user(body: UserCreate):
    user = user_service.create_user(body.name, body.email)
    return UserResponse(userId=user.user_id, name=user.name, email=user.email)


@router.post("/accounts", response_model=AccountResponse, status_code=201)
def create_account(body: AccountCreate):
    account = account_service.create_account(body.userId, body.accountType)
    return to_account_response(account)


@router.get("/accounts/{account_id}", response_model=AccountResponse)
def get_account(account_id: int):
    return to_account_response(account_service.get_account(account_id))


@router.post("/accounts/{account_id}/deposit", response_model=AccountResponse)
def deposit(account_id: int, body: AmountRequest):
    return to_account_response(account_service.deposit(account_id, body.amount))


@router.post("/accounts/{account_id}/withdraw", response_model=AccountResponse)
def withdraw(account_id: int, body: AmountRequest):
    return to_account_response(account_service.withdraw(account_id, body.amount))


@router.get("/accounts/{account_id}/transactions", response_model=list[TransactionResponse])
def get_transactions(account_id: int):
    return [
        TransactionResponse(
            txnId=t.txn_id,
            type=t.txn_type,
            amount=float(t.amount),
            date=t.created_at.date(),
        )
        for t in account_service.get_transactions(account_id)
    ]