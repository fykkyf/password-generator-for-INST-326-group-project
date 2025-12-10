import secrets 
from password_dictionary import PASSWORD_CHARS

# Build the allowed character pool:
#   - uppercase letters
#   - lowercase letters
#   - symbols (special characters)
ALLOWED_CHARS = (
    PASSWORD_CHARS["uppercase"]
    + PASSWORD_CHARS["lowercase"]
    + PASSWORD_CHARS["symbols"]
)

MIN_LENGTH = 15
MAX_LENGTH = 32


def generate_password(length: int) -> str:
    """Generate a single password of the given length."""
    return "".join(secrets.choice(ALLOWED_CHARS) for _ in range(length))


def get_int(prompt: str) -> int:
    """Safely get an integer from the user."""
    while True:
        value = input(prompt).strip()
        if not value.isdigit():
            print("Please enter a whole number.")
            continue
        return int(value)


def main():
    print("=== Password Generator ===")
    print(f"Password length must be between {MIN_LENGTH} and {MAX_LENGTH} characters.\n")

    # Ask for password length and keep asking until it's valid
    while True:
        length = get_int("Enter desired password length: ")

        if length < MIN_LENGTH or length > MAX_LENGTH:
            print(f"Error: length must be between {MIN_LENGTH} and {MAX_LENGTH}.\n")
        else:
            break

    # Ask how many passwords to generate
    while True:
        count = get_int("How many passwords would you like to generate? ")
        if count <= 0:
            print("Error: number of passwords must be at least 1.\n")
        else:
            break

    print("\nGenerated passwords:\n")
    for i in range(1, count + 1):
        pwd = generate_password(length)
        print(f"{i}: {pwd}")



    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()