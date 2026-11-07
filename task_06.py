"""Task 06: Banking ledger using OOP and immutable transaction records."""

from dataclasses import dataclass
from itertools import count

_transaction_ids = count(1)

@dataclass(frozen=True)
class Transaction:
    transaction_id: int
    action: str
    amount: float
    resulting_balance: float

class Account:
    def __init__(self, account_id, opening_balance=0):
        if opening_balance < 0:
            raise ValueError("Opening balance cannot be negative")
        self.account_id = account_id
        self._balance = float(opening_balance)
        self._statement = []

    @property
    def balance(self):
        return self._balance

    @property
    def statement(self):
        return tuple(self._statement)

    @staticmethod
    def _validate_amount(amount):
        if not isinstance(amount, (int, float)) or isinstance(amount, bool) or amount <= 0:
            raise ValueError("Amount must be a positive number")

    def _record(self, action, amount):
        self._statement.append(Transaction(
            next(_transaction_ids), action, float(amount), self._balance
        ))

    def deposit(self, amount):
        self._validate_amount(amount)
        self._balance += amount
        self._record("deposit", amount)

    def withdraw(self, amount):
        self._validate_amount(amount)
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount
        self._record("withdrawal", amount)

    def get_statement(self):
        return self.statement

class Bank:
    def __init__(self):
        self.accounts = {}

    def add_account(self, account):
        if account.account_id in self.accounts:
            raise ValueError("Account already exists")
        self.accounts[account.account_id] = account

    def _get(self, account_id):
        if account_id not in self.accounts:
            raise KeyError(f"Account does not exist: {account_id}")
        return self.accounts[account_id]

    def transfer(self, source_id, destination_id, amount):
        Account._validate_amount(amount)
        source = self._get(source_id)
        destination = self._get(destination_id)
        if source is destination:
            raise ValueError("Cannot transfer to the same account")
        if source.balance < amount:
            raise ValueError("Insufficient funds")

        # All validation happens before either balance changes.
        source._balance -= amount
        destination._balance += amount
        source._record("transfer_out", amount)
        destination._record("transfer_in", amount)


if __name__ == "__main__":
    bank = Bank()
    a, b = Account("A", 1000), Account("B", 200)
    bank.add_account(a)
    bank.add_account(b)
    bank.transfer("A", "B", 350)
    print(a.balance, b.balance)  # 650.0 550.0
