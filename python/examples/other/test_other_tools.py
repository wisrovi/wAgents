import os
import json


def example_function():
    # Code with various style issues for pre-commit hooks
    data = {"name": "test", "value": 123}
    
    # Trailing whitespace    
    x = 1
    
    # Mixed tabs and spaces
	y = 2  # Tab here
    
    # File without newline at end
    return data


if __name__ == "__main__":
    result = example_function()
    print(json.dumps(result))