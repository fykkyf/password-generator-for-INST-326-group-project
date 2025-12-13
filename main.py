from PasswordManager import PasswordManager

#15 to 32 chars
def print_entries(entries):
    """Print password entries"""
    if not entries:
        print("No results found")
        return

    for e in entries:
        print(
            f"ID={e['id']} | Site={e['site']} | Username={e['username']} | "
            f"Password={e['password']} | Created={e['created_at']}"
        )


def main():
    """Run the password manager."""
    pm = PasswordManager()

    while True:
        print("\n Welcome To Our Password Generator!")
        print("1) Add password")
        print("2) Generate password")
        print("3) View all passwords")
        print("4) Search by site")
        print("5) Update password by ID")
        print("6) Delete password by ID")
        print("7) Export to CSV")
        print("8) Import from CSV")
        print("0) Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            site = input("Site: ").strip()
            username = input("Username: ").strip()
            password = input("Password: ").strip()

            strength = pm.add_password(site, username, password)
            print(f"Saved. Strength: {strength}")

        elif choice == "2":
            while True:
                length = int(input("Password length (15-32): ").strip())
                if 15 <= length <= 32:
                    break
                print("Invalid length. Enter a number from 15 to 32.")
                
            print("Generated password:", pm.generate_password(length))

        elif choice == "3":
            print_entries(pm.get_all_passwords())

        elif choice == "4":
            site = input("Site to search: ").strip()
            print_entries(pm.get_passwords_for_site(site))

        elif choice == "5":
            entry_id = int(input("Entry ID to update: ").strip())
            new_password = input("New password: ").strip()
            strength = pm.update_password(entry_id, new_password)
            print(f"Updated. New strength: {strength}")

        elif choice == "6":
            entry_id = int(input("Entry ID to delete: ").strip())
            pm.remove_password(entry_id)
            print("Password deleted.")

        elif choice == "7":
            path = input("CSV export path (e.g., passwords.csv): ").strip()
            pm.export_csv(path)
            print(f"Exported to {path}")

        elif choice == "8":
            path = input("CSV import path: ").strip()
            pm.import_csv(path)
            print(f"Imported from {path}")

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()