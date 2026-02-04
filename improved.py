import json
import random
import string
from pathlib import Path
from copy import deepcopy


class Bank:
    DATABASE = "data.json"
    MIN_AGE = 18
    MAX_DEPOSIT = 10000
    MAX_WITHDRAW = 5000

    def __init__(self):
        self.data = self._load_data()

    # ---------- FILE HANDLING ----------
    def _load_data(self):
        if Path(self.DATABASE).exists():
            with open(self.DATABASE, "r") as file:
                return json.load(file)
        return []

    def _update_file(self):
        with open(self.DATABASE, "w") as file:
            json.dump(self.data, file, indent=4)

    # ---------- HELPERS ----------
    def _generate_account_number(self):
        while True:
            acc = "".join(random.choices(
                string.ascii_uppercase + string.digits, k=8
            ))
            if not any(user["account_no"] == acc for user in self.data):
                return acc

    def authenticate(self, acc_no, pin):
        for user in self.data:
            if user["account_no"] == acc_no and user["pin"] == pin:
                return user
        return None

    # ---------- CORE OPERATIONS ----------
    def create_account(self, name, age, email, pin):
        if age < self.MIN_AGE or len(str(pin)) != 4:
            return False, "Age must be ≥18 and PIN must be 4 digits"

        account = {
            "name": name,
            "age": age,
            "email": email,
            "pin": pin,
            "account_no": self._generate_account_number(),
            "balance": 0
        }

        self.data.append(account)
        self._update_file()
        return True, account

    def deposit(self, user, amount):
        if amount <= 0 or amount > self.MAX_DEPOSIT:
            return False, "Invalid deposit amount"

        user["balance"] += amount
        self._update_file()
        return True, "Deposit successful"

    def withdraw(self, user, amount):
        if amount <= 0 or amount > self.MAX_WITHDRAW:
            return False, "Invalid withdrawal amount"
        if user["balance"] < amount:
            return False, "Insufficient balance"

        user["balance"] -= amount
        self._update_file()
        return True, "Withdrawal successful"

    def update_details(self, user, name=None, email=None, pin=None):
        old_data = deepcopy(user)

        if name:
            user["name"] = name
        if email:
            user["email"] = email
        if pin:
            if len(str(pin)) != 4:
                return False, "PIN must be 4 digits"
            user["pin"] = pin

        self._update_file()
        return True, {"old": old_data, "new": user}

    def delete_account(self, user):
        self.data.remove(user)
        self._update_file()
        return True
