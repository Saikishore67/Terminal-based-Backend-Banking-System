from database import get_db_connection, add_customer
from models import Customer, Account, Transaction
from mysql.connector import Error
import datetime

#=============CUSTOMER SERVICES===============
def create_new_customer(name, address, email, phone):
    customer_id = add_customer(name, address, email, phone)
    if customer_id:
        return Customer(name, customer_id, address, email, phone)
    return None

def get_all_customers():
    conn = get_db_connection()
    if conn is None:
        return []

    cursor = conn.cursor()
    try:
       cursor.execute("SELECT id, name, address, email, phone FROM customers")
       rows = cursor.fetchall()

       customers = []
       for row in rows:
           customer_obj = Customer(
               id=row[0],
               name=row[1],
               address=row[2],
               email=row[3],
               phone=row[4]
           )
           customers.append(customer_obj)

       return customers
    except Error as e:
        print(f"Error fetching customers: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def get_customer_by_id(customer_id):
    conn = get_db_connection()
    if conn is None:
        return None

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, name, address, email, phone FROM customers WHERE id = %s", (customer_id,))
        row = cursor.fetchone()

        if row:
            return Customer(
                id=row[0],
                name=row[1],
                address=row[2],
                email=row[3],
                phone=row[4]
            )
        return None
    except Error as e:
        print(f"Error fetching customer: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

#=====================ACCOUNT SERVICES===================
def create_account_for_customer(customer_id, account_type, initial_deposit=0.0):
    conn = get_db_connection()
    if conn is None:
        return None

    cursor = conn.cursor()
    try:
        conn.start_transaction()

        # Insert into accounts table (initial deposit is optional)
        if initial_deposit > 0:
            cursor.execute(
                "INSERT INTO accounts (account_type, balance, customer_id) VALUES (%s, %s, %s)",
                (account_type, initial_deposit, customer_id)
            )
        else:
            cursor.execute(
                "INSERT INTO accounts (account_type, customer_id) VALUES (%s, %s)",
                (account_type, customer_id)
            )

        account_id = cursor.lastrowid

        # Log initial deposit transaction
        if initial_deposit > 0:
            cursor.execute(
                "INSERT INTO transactions (type, amount, timestamp, account_id) VALUES (%s, %s, %s, %s)",
                ("DEPOSIT", initial_deposit, datetime.datetime.now(), account_id)
            )

        conn.commit()

        return Account(
            id=account_id,
            account_type=account_type,
            balance=initial_deposit,
            customer_id=customer_id
        )

    except Error as e:
        conn.rollback()
        print(f"Error creating account: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def deposit_to_account(account_id, amount):
    conn = get_db_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
        conn.start_transaction()
        cursor.execute("UPDATE accounts SET balance = balance + %s WHERE id = %s", (amount, account_id))
        cursor.execute(
            "INSERT INTO transactions (type, amount, timestamp, account_id) VALUES (%s, %s, %s, %s)",
            ("DEPOSIT", amount, datetime.datetime.now(), account_id)
        )

        conn.commit()
        print(f"Succesfully deposited ${amount:.2f}")
        return True
    except Error as e:
        print(f"Error updating transaction: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


def get_accounts_by_customer(customer_id):
    conn = get_db_connection()
    if conn is None:
        return []

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, account_type, balance, customer_id FROM accounts WHERE customer_id = %s",
                       (customer_id,))
        rows = cursor.fetchall()

        accounts = []
        for row in rows:
            account = Account(
                id=row[0],
                account_type=row[1],
                balance=float(row[2]),
                customer_id=row[3]
            )
            accounts.append(account)

        return accounts

    except Error as e:
        print(f"Error fetching accounts: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

# ============= TRANSACTION SERVICES =============

def withdraw_from_account(account_id, amount):
    conn = get_db_connection()
    if conn is None:
        return False

    try:
        conn.start_transaction()
        cursor = conn.cursor()

        # Lock the row for update
        cursor.execute("SELECT balance FROM accounts WHERE id = %s FOR UPDATE", (account_id,))
        result = cursor.fetchone()

        if not result:
            print("Account not found")
            conn.rollback()
            return False

        current_balance = float(result[0])

        if current_balance < amount:
            print(f"Insufficient funds. Current balance: ₹{current_balance:.2f}")
            conn.rollback()
            return False

        # Update balance
        cursor.execute("UPDATE accounts SET balance = balance - %s WHERE id = %s", (amount, account_id))

        # Record the transaction
        cursor.execute(
            "INSERT INTO transactions (type, amount, timestamp, account_id) VALUES (%s, %s, %s, %s)",
            ("WITHDRAWAL", amount, datetime.datetime.now(), account_id)
        )

        conn.commit()
        print(f"Successfully withdrew ${amount:.2f}")
        return True

    except Error as e:
        try:
            conn.rollback()
        except:
            pass
        print(f"Error during withdrawal: {e}")
        return False

    finally:
        try:
            cursor.close()
        except:
            pass
        conn.close()



def get_account_details(account_id):
    conn = get_db_connection()
    if conn is None:
        return None

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, account_type, balance, customer_id FROM accounts WHERE id = %s", (account_id,))
        account_row = cursor.fetchone()

        if not account_row:
            return None

        cursor.execute(
            "SELECT id, type, amount, timestamp, account_id FROM transactions WHERE account_id = %s ORDER BY timestamp DESC LIMIT 10",
            (account_id,)
        )
        transaction_rows = cursor.fetchall()

        account = Account(
            id=account_row[0],
            account_type=account_row[1],
            balance=float(account_row[2]),
            customer_id=account_row[3]
        )

        for tx_row in transaction_rows:
            transaction = Transaction(
                id=tx_row[0],
                type=tx_row[1],
                amount=float(tx_row[2]),
                timestamp=tx_row[3],
                account_id=tx_row[4]
            )
            account.transactions.append(transaction)

        return account

    except Error as e:
        print(f"Error fetching account details: {e}")
        return None
    finally:
        cursor.close()
        conn.close()