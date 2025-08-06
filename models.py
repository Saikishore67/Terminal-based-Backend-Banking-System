import datetime

class Customer:
    def __init__(self, name, id, address, email, phone):
        self.name = name
        self.id = id
        self.address = address
        self.email = email
        self.phone = str(phone)
        self.accounts = []

class Account:
    def __init__(self, id, account_type, balance, customer_id):
        self.id = id
        self.account_type = account_type
        self.balance = balance
        self.customer_id = customer_id
        self.transactions = []

class Transaction:
    def __init__(self,id, type, amount, timestamp, account_id):
        self.id = id
        self.type = type
        self.amount = amount
        self.timestamp = timestamp or datetime.datetime.utcnow()
        self.account_id = account_id
