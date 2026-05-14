import tkinter as tk
from tkinter import messagebox
from decimal import Decimal, InvalidOperation
from datetime import datetime
import hashlib

# ----- SECURITY -----
def hash_pin(pin):
    return hashlib.sha256(pin.encode()).hexdigest()

STORED_PIN_HASH = hash_pin("1234")

# ----- STATE -----
balance = Decimal("100.00")
withdrawn_today = Decimal("0.00")
DAILY_LIMIT = Decimal("200.00")
PER_TRANSACTION_LIMIT = Decimal("100.00")
history = []

# ----- FUNCTIONS -----
def log_transaction(message):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history.append(f"[{time}] {message}")

def format_money(amount):
    return f"₹{amount:.2f}"

def get_amount(entry):
    try:
        value = Decimal(entry.get())
        if value <= 0:
            raise InvalidOperation
        return value
    except:
        messagebox.showerror("Error", "Enter a valid positive number")
        return None

# ----- LOGIN -----
def check_login():
    entered = pin_entry.get()
    if hash_pin(entered) == STORED_PIN_HASH:
        login_frame.pack_forget()
        main_frame.pack()
    else:
        messagebox.showerror("Error", "Incorrect PIN")

# ----- ATM OPERATIONS -----
def show_balance():
    messagebox.showinfo("Balance", f"Current Balance: {format_money(balance)}")

def deposit():
    global balance
    amount = get_amount(amount_entry)
    if amount:
        balance += amount
        log_transaction(f"Deposited {format_money(amount)}")
        messagebox.showinfo("Success", "Deposit successful")

def withdraw():
    global balance, withdrawn_today
    amount = get_amount(amount_entry)
    if not amount:
        return

    if amount > PER_TRANSACTION_LIMIT:
        messagebox.showwarning("Limit", "Exceeds per transaction limit")
        return

    if withdrawn_today + amount > DAILY_LIMIT:
        messagebox.showwarning("Limit", "Daily limit exceeded")
        return

    if amount > balance:
        messagebox.showerror("Error", "Insufficient balance")
        return

    balance -= amount
    withdrawn_today += amount
    log_transaction(f"Withdrew {format_money(amount)}")
    messagebox.showinfo("Success", "Withdrawal successful")

def show_history():
    history_window = tk.Toplevel(root)
    history_window.title("Transaction History")

    text = tk.Text(history_window, width=50, height=15)
    text.pack()

    if not history:
        text.insert(tk.END, "No transactions yet.")
    else:
        for item in history:
            text.insert(tk.END, item + "\n")

# ----- GUI SETUP -----
root = tk.Tk()
root.title("ATM System")
root.geometry("400x400")

# ----- LOGIN FRAME -----
login_frame = tk.Frame(root)

tk.Label(login_frame, text="Enter PIN", font=("Arial", 16)).pack(pady=10)
pin_entry = tk.Entry(login_frame, show="*")
pin_entry.pack(pady=10)

tk.Button(login_frame, text="Login", command=check_login).pack(pady=10)

login_frame.pack()

# ----- MAIN FRAME -----
main_frame = tk.Frame(root)

tk.Label(main_frame, text="ATM Menu", font=("Arial", 16)).pack(pady=10)

amount_entry = tk.Entry(main_frame)
amount_entry.pack(pady=10)

tk.Button(main_frame, text="Check Balance", command=show_balance).pack(pady=5)
tk.Button(main_frame, text="Deposit", command=deposit).pack(pady=5)
tk.Button(main_frame, text="Withdraw", command=withdraw).pack(pady=5)
tk.Button(main_frame, text="Transaction History", command=show_history).pack(pady=5)
tk.Button(main_frame, text="Exit", command=root.quit).pack(pady=10)

# ----- RUN -----
root.mainloop()