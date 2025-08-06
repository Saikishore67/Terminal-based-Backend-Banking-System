from cli import main_menu, create_new_customer_cli, select_existing_customer


def main():
    while True:
        choice = main_menu()

        if choice == "1":
            create_new_customer_cli()
        elif choice == "2":
            select_existing_customer()
        elif choice == "3":
            print("Thank you for using our services. - SKR Bank.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
