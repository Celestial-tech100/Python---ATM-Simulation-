from decimal import Decimal, InvalidOperation
from datetime import datetime
import hashlib

# ----- CONFIG -----
# Store hashed PIN instead of plain text
def hash_pin(pin):
    return hashlib.sha256(pin.encode()).hexdigest()

STORED_PIN_HASH = hash_pin("1234")

MAX_ATTEMPTS = 3
DAILY_LIMIT = Decimal("200.00")
PER_TRANSACTION_LIMIT = Decimal("100.00")

# ----- STATE -----
balance = Decimal("100.00")
withdrawn_today = Decimal("0.00")
history = []


# ----- HELPERS -----
def format_money(amount):
    return f"₹{amount:.2f}"


def log_transaction(message):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history.append(f"[{time}] {message}")


def get_amount(prompt):
    try:
        amount = Decimal(input(prompt))
        if amount <= 0:
            print("Amount must be positive.")
            return None
        return amount
    except InvalidOperation:
        print("Invalid input! Please enter a valid number.")
        return None


# ----- LOGIN WITH ENCRYPTION -----
def login():
    for attempt in range(MAX_ATTEMPTS):
        entered_pin = input("Enter your PIN: ")
        if hash_pin(entered_pin) == STORED_PIN_HASH:
            print("Login successful!\n")
            return True
        else:
            print(f"Incorrect PIN. Attempts left: {MAX_ATTEMPTS - attempt - 1}")
    print("Account locked due to too many failed attempts.")
    return False


# ----- ATM OPERATIONS -----
def check_balance():
    print(f"Current Balance: {format_money(balance)}")


def deposit():
    global balance
    amount = get_amount("Enter amount to deposit: ₹")
    if amount:
        balance += amount
        log_transaction(f"Deposited {format_money(amount)}")
        print(f"{format_money(amount)} deposited successfully.")


def withdraw():
    global balance, withdrawn_today

    amount = get_amount("Enter amount to withdraw: ₹")
    if not amount:
        return

    if amount > PER_TRANSACTION_LIMIT:
        print(f"Per transaction limit is {format_money(PER_TRANSACTION_LIMIT)}")
        return

    if withdrawn_today + amount > DAILY_LIMIT:
        remaining = DAILY_LIMIT - withdrawn_today
        print(f"Daily limit exceeded! You can withdraw only {format_money(remaining)} more today.")
        return

    if amount > balance:
        print("Insufficient balance.")
        return

    balance -= amount
    withdrawn_today += amount
    log_transaction(f"Withdrew {format_money(amount)}")
    print(f"{format_money(amount)} withdrawn successfully.")


def show_history():
    print("\n--- Transaction History ---")
    if not history:
        print("No transactions yet.")
    else:
        for i, entry in enumerate(history, 1):
            print(f"{i}. {entry}")


# ----- MENU -----
def atm_menu():
    while True:
        print("\n----- ATM MENU -----")
        print("1. Check Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Transaction History")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            check_balance()
        elif choice == "2":
            deposit()
        elif choice == "3":
            withdraw()
        elif choice == "4":
            show_history()
        elif choice == "5":
            print("Thank you for using the ATM!")
            break
        else:
            print("Invalid choice. Try again.")


# ----- RUN -----
if login():
    atm_menu()