import re



def validate_email(email):
    # Regex matching the basic pattern of an email address
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def valdate_integer(number: str) -> int:
    while True:
        try:
            return int(input(number))
        except ValueError:
            print("Invalid input! Please enter a whole number.")