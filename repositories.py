from decimal import Decimal
from typing import Optional

from models import Account, Transaction, User


class UserRepository:
    def __init__(self):
        self._users: dict[int, User] = {}
        self._next_id = 1

    def save(self, name: str, email: str) -> User:
        user = User(user_id=self._next_id, name=name, email=email)
        self._users[user.user_id] = user
        self._next_id += 1
        return user

    def find_by_id(self, user_id: int) -> Optional[User]:
        return self._users.get(user_id)

    def find_by_email(self, email: str) -> Optional[User]:
        return next((u for u in self._users.values() if u.email == email), None)


class AccountRepository:
    def __init__(self):
        self._accounts: dict[int, Account] = {}
        self._next_id = 1

    def save(self, user_id: int, account_type: str) -> Account:
        account = Account(account_id=self._next_id, user_id=user_id, account_type=account_type)
        self._accounts[account.account_id] = account
        self._next_id += 1
        return account

    def find_by_id(self, account_id: int) -> Optional[Account]:
        return self._accounts.get(account_id)

    def update_balance(self, account_id: int, new_balance: Decimal) -> None:
        self._accounts[account_id].balance = new_balance


class TransactionRepository:
    def __init__(self):
        self._transactions: list[Transaction] = []
        self._next_id = 1

    def save(self, account_id: int, txn_type: str, amount: Decimal) -> Transaction:
        txn = Transaction(txn_id=self._next_id, account_id=account_id, txn_type=txn_type, amount=amount)
        self._transactions.append(txn)
        self._next_id += 1
        return txn

    def find_by_account(self, account_id: int) -> list[Transaction]:
        return [t for t in self._transactions if t.account_id == account_id]