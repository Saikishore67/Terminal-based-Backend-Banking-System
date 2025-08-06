from services import *

def main_menu():
    while True:
        print("============MAIN MENU==========")
        print("1. Create new Customer")
        print("2. Select existing Customer")
        print("3. Exit")
        return input("Enter your choice: ")

def create_new_customer_cli():
    print("==========CREATE NEW CUSTOMER=========")
    name = input("Enter customer name: ")
    address = input("Enter customer address: ")
    email = input("Enter customer email: ")
    phone = input("Enter customer phone: ")

    customer = create_new_customer(name, address, email, phone)

    if customer:
        print(f"Customer created successfully: {customer.id}")
    else:
        print(f"Error creating customer")

def select_existing_customer():
    customers = get_all_customers()
    if not customers:
        print("No customer found")
        return

    print("=========SELECT CUSTOMER=========")
    for customer in customers:
        print(f"NAME: {customer.name}, ID: {customer.id}, EMAIL: {customer.email}")

    selected_id = input("Enter customer id to select: ")
    customer = get_customer_by_id(selected_id)

    if not customer:
        print("Customer not found.")
        input("Press Enter to continue...")
        return

    print(f"Selected customer: {customer.name} (ID: {customer.id})")
    customer_menu(customer)

def customer_menu(customer):
    while True:
        print(f"=========CUSTOMER MENU ({customer.name})==========")
        print("1. Create account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Check balance")
        print("5. Back to main menu")
        choice = input("Enter choice: ")

        if choice == "1":
            account_type = input("Enter account type(savings/current): ")
            try:
                initial_amount = float(input("Enter initial deposit (0 or skip): "))
            except ValueError:
                print("Invalid input")
                return

            account = create_account_for_customer(customer.id, account_type, initial_amount)
            if account:
                print(f"Account created successfully. Account ID: {account.id}")
            else:
                print("Error creating account")
        elif choice == "2":
            acc_id = input("Enter account ID to which to deposit: ")
            try:
                amount = float(input("Enter amount to deposit: "))
            except ValueError:
                print("Invalid input")
                return

            if deposit_to_account(acc_id, amount):
                print(f"Deposit successful.")
            else:
                print("Error while depositing amount")

        elif choice == "3":
            acc_id = input("Enter account ID to which to withdraw: ")
            try:
                amount = float(input("Enter amount to withdraw: "))
            except ValueError:
                print("Invalid input")

            if withdraw_from_account(acc_id, amount):
                print(f"Withdraw successful.")
            else:
                print("Error while withdrawing or insufficient balance.")

        elif choice == "4":
            acc_id = input("Enter Account ID to view details: ")
            account = get_account_details(acc_id)
            if account:
                print(f"\n--- Account ID: {account.id} ---")
                print(f"Type     : {account.account_type}")
                print(f"Balance  : ${account.balance:.2f}")
                print(f"Customer : {account.customer_id}")
                print("Recent Transactions:")
                for tx in account.transactions:
                    print(f"{tx.timestamp} | {tx.type} | ${tx.amount:.2f}")
            else:
                print("Account not found.")

        elif choice == "5":
            break
        else:
            print("Invalid option.")
        input("Press Enter to continue...")

if __name__ == "__main__":
    main_menu()



