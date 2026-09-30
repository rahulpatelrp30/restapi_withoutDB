from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=3, max_length=100)


class UserResponse(BaseModel):
    userId: int
    name: str
    email: str


class AccountCreate(BaseModel):
    userId: int
    accountType: Literal["SAVINGS", "CURRENT"]


class AmountRequest(BaseModel):
    amount: Decimal


class AccountResponse(BaseModel):
    accountId: int
    userName: str
    accountType: str
    balance: float


class TransactionResponse(BaseModel):
    txnId: int
    type: str
    amount: float
    date: date