from bank_account import BankAccount, InsufficientFundsError, InvalidAmountError

# Create Account
a1 = BankAccount("Vandana", initial_balance=5000)
a2 = BankAccount("Amit", initial_balance=2000, acc_type="current")

print(a1)
print(a2)

a1.deposit(1500, note='salary')
print("After deposit:", a1.deposit)

# withdraw

try:
    a2.withdraw(3000)
except InsufficientFundsError as e:
    print("Withdrawal failed:", e)

# Transfer
a1.transfer_to(a2, 1000, note='repayment')
print("Balance:", a1.balance, a2.balance)

# Interest
interest = a2.apply_interest(5.0)
print("Interest credited:", interest)

# Transaction history
for tx in a2.get_transaction_history():
    print(tx) 