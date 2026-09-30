from decimal import Decimal


class NotFoundError(Exception):
    pass


class BusinessRuleError(Exception):
    pass


class UserService:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def create_user(self, name: str, email: str):
        if self.user_repo.find_by_email(email):
            raise BusinessRuleError("Email is already registered")
        return self.user_repo.save(name, email)

    def get_user(self, user_id: int):
        user = self.user_repo.find_by_id(user_id)
        if user is None:
            raise NotFoundError(f"User {user_id} not found")
        return user


class AccountService:
    def __init__(self, user_repo, account_repo, txn_repo):
        self.user_repo = user_repo
        self.account_repo = account_repo
        self.txn_repo = txn_repo

    def create_account(self, user_id: int, account_type: str):
        if self.user_repo.find_by_id(user_id) is None:
            raise NotFoundError(f"User {user_id} not found")
        return self.account_repo.save(user_id, account_type)

    def get_account(self, account_id: int):
        account = self.account_repo.find_by_id(account_id)
        if account is None:
            raise NotFoundError(f"Account {account_id} not found")
        return account

    def deposit(self, account_id: int, amount: Decimal):
        # Business rule: deposit amount must be positive
        if amount <= 0:
            raise BusinessRuleError("Deposit amount must be positive")
        account = self.get_account(account_id)
        self.account_repo.update_balance(account_id, account.balance + amount)
        # Business rule: record every deposit
        self.txn_repo.save(account_id, "DEPOSIT", amount)
        return self.get_account(account_id)

    def withdraw(self, account_id: int, amount: Decimal):
        if amount <= 0:
            raise BusinessRuleError("Withdrawal amount must be positive")
        account = self.get_account(account_id)
        # Business rule: cannot withdraw more than balance
        if amount > account.balance:
            raise BusinessRuleError("Insufficient balance")
        self.account_repo.update_balance(account_id, account.balance - amount)
        self.txn_repo.save(account_id, "WITHDRAW", amount)
        return self.get_account(account_id)

    def get_transactions(self, account_id: int):
        self.get_account(account_id)  # raises 404 if the account doesn't exist
        return self.txn_repo.find_by_account(account_id)