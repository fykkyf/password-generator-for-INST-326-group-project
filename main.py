from PasswordManager import PasswordManager


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
def _prompt_int(prompt: str) -> int:
    """Prompt until user enters a valid integer (or raises KeyboardInterrupt)."""
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("Please enter a valid number.")

def main():
    """Run the password manager."""
    pm = PasswordManager()

    while True:
        print("\n Welcome To Our Password Genarator!")
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
            # Keep prompting until user enters a strong-enough password, or cancels.
            while True:
                password = input("Password: ").strip()
                if password == "0":
                    print("Canceled. Nothing saved.")
                    break
                try:
                    strength = pm.add_password(site, username, password)
                    print(f"Saved. Strength: {strength}")
                    break
                except ValueError as e:
                    print(f"⚠️ {e}")
                    print("This password will NOT be saved.")
                    print("Please enter a stronger password, or type 0 to cancel.")

        elif choice == "2":
            length = int(input("Password length: ").strip())
            print("Generated password:", pm.generate_password(length))

        elif choice == "3":
            print_entries(pm.get_all_passwords())

        elif choice == "4":
            site = input("Site to search: ").strip()
            print_entries(pm.get_passwords_for_site(site))


        elif choice == "5":
            entry_id = _prompt_int("Entry ID to update: ")
            # Keep prompting until user enters a strong-enough password, or cancels.
            while True:
                new_password = input("New password (type 0 to cancel): ").strip()
                if new_password == "0":
                    print("Canceled. No update.")
                    break
                try:
                    strength = pm.update_password(entry_id, new_password)
                    print(f"Updated. New strength: {strength}")
                    break
                except ValueError as e:
                    print(f"⚠️ {e}")
                    print("Update rejected. Please enter a stronger password, or type 0 to cancel.")

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
            try:
                result = pm.import_csv(path)
                if isinstance(result, tuple) and len(result) == 2:
                    imported, skipped = result
                    print(f"Imported {imported} rows. Skipped {skipped} weak rows.")
                else:
                    print(f"Imported from {path}")
            except ValueError as e:
                print(f"⚠️ Import failed: {e}")

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting program. Goodbye!")