import mysql.connector
from mysql.connector import Error
import datetime


db_config = {
    "host": "localhost",
    "user": "user-name",      # Replace with your MySQL username (e.g., "root")
    "password": "your-password",  # Replace with your MySQL password
    "database": "skr_bank_db"     # The database you just created
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

def init_db():
    conn = get_db_connection()
    if conn is None:
        print("Could not connect to the database. Aborting initialization.")
        return

    cursor = conn.cursor()
    print("Successfully connected to the database. Creating tables...")

    try:
        # Create Customers Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            address VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            phone VARCHAR(50) NOT NULL 
        );
        """)

        # Create Accounts Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            account_type VARCHAR(255) NOT NULL,
            balance DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
            customer_id INT,
            FOREIGN KEY (customer_id) REFERENCES customers (id) ON DELETE CASCADE
        );
        """)

        # Create Transactions Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            type VARCHAR(50) NOT NULL,
            amount DECIMAL(15, 2) NOT NULL,
            timestamp DATETIME NOT NULL,
            account_id INT,
            FOREIGN KEY (account_id) REFERENCES accounts (id) ON DELETE CASCADE
        );
        """)

        conn.commit()
        print("Database tables created or already exist.")

    except Error as e:
        print(f"Error creating tables: {e}")
    finally:
        cursor.close()
        conn.close()
        print("Database connection closed.")



def add_customer(name, address, email, phone):
    """Adds a new customer to the database."""
    conn = get_db_connection()
    if conn is None:
        return None

    cursor = conn.cursor()
    sql = "INSERT INTO customers (name, address, email, phone) VALUES (%s, %s, %s, %s)"
    val = (name, address, email, phone)

    try:
        cursor.execute(sql, val)
        conn.commit()
        print(f"Customer '{name}' added successfully.")
        return cursor.lastrowid # Returns the ID of the new customer
    except Error as e:
        print(f"Error adding customer: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    # This block allows you to run this file directly to set up the database
    print("Initializing database...")
    init_db()
