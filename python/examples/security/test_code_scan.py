import os
import subprocess


def vulnerable_function(user_input):
    # SQL injection vulnerability
    query = "SELECT * FROM users WHERE name = '" + user_input + "'"
    return query


def another_vulnerability():
    # Use of eval() - dangerous
    user_code = "print('hello')"
    eval(user_code)


def hardcoded_password():
    # Hardcoded credentials
    password = "admin123"
    return password


def insecure_file_operation():
    # Path traversal vulnerability
    filename = "../../../etc/passwd"
    with open(filename, "r") as f:
        return f.read()


if __name__ == "__main__":
    user_input = input("Enter your name: ")
    vulnerable_function(user_input)
    another_vulnerability()
    hardcoded_password()
    insecure_file_operation()
