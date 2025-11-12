from typing import List, Dict
import datetime

class InsufficientFundsError(Exception):
    """Raised when a withdraw or transfer requests more than available funds."""
    pass

class InvalidAmountError(Exception):
    """Raised when a provided amount is invalid (<= 0)."""
    pass


class BankAccount:
    _next_acc_no = 100000001

    def __init__(self, owner: str, initial_balance: float = 0.0, acc_type: str = "saving"):
        if initial_balance < 0:
            raise InvalidAmountError("Initial balance cannot be negative.")
        self.owner = owner
        self._acc_no = BankAccount._next_acc_no
        BankAccount._next_acc_no += 1

        self._acc_type = acc_type.lower()
        self.__balance = float(initial_balance)
        self._transactions: List[Dict] = []
        if initial_balance > 0:
            self._add_transaction("deposit", initial_balance, "initial deposit")


    @property
    def acc_no(self) -> int:
        return self._acc_no
    
    @property
    def acc_type(self) -> str:
        return self. _acc_type
    
    @property
    def balance(self) -> float:
        return self.__balance
    
    def _add_transaction(self, ttype: str, amount: float, note: str = ""):
        self._add_transaction.append({
            "type": ttype,
            "amount": float(amount),
            "note" : note,
            "time" : datetime.datatime.now()
        })

    def deposit(self, amount: float, note: str = "") -> float:
        """Deposit amount into account. Returns new balance."""
        if amount <= 0:
            raise InvalidAmountError("Deposit amount must be positive.")
        self.__balance += amount
        self._add_transaction("deposit", amount, note)
        return self.__balance
    
    def withdraw(self, amount: float, note: str = "") -> float:
        """Withdraw amount if sufficient funds. Returns new balance."""
        if amount < 0:
            raise InvalidAmountError("Withdrawal amount must be positive.")
        if amount > self.__balance:
            raise InsufficientFundsError("Insufficient funds for withdrawal.")
        self.__balance -= amount
        self._add_transaction("Withdraw", amount, note)
        return self.__balance
    
    def transfer_to(self, target_account: "BankAccount", amount: float, note: str = ""):
        """Transfer amount to another BankAccount."""
        if not isinstance(target_account, BankAccount):
            raise TypeError("target_account must be a BankAccount instance.")
        if amount <= 0:
            raise InvalidAmountError("Transfer amount must be positive.")
        if amount > self.__balance:
            raise InsufficientFundsError("Insufficient funds for transfer.")
        self.__balance -= amount
        target_account.__receive_transfer(amount, self, note)
        self._add_transaction("transfer_out", amount, f"to {target_account.acc_no}. {note}")

    def __receive_transfer(self, amount: float, source_account: "BankAccount", note: str = ""):
        """Private helper to receive transferred funds."""
        self.__balance += amount
        self._add_transaction("transfer_in", amount, f"from {source_account.acc_no}. {note}")
