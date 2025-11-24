# This file imports libraries with known vulnerabilities for testing
import requests  # Version with known vulnerability
import urllib3  # Version with known vulnerability
import django  # Version with known vulnerability
import flask  # Version with known vulnerability


def use_vulnerable_libraries():
    # Code that uses the vulnerable libraries
    response = requests.get("https://example.com")
    return response.status_code


if __name__ == "__main__":
    use_vulnerable_libraries()
