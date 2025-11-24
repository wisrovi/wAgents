import os
import sys


def bad_function():
    # Line too long
    very_long_variable_name_that_exceeds_the_maximum_line_length_limit_and_should_be_split_across_multiple_lines = "test"

    # Unused variable
    unused_var = "this is never used"

    # Missing whitespace after operator
    x = 1 + 2

    # Import not at top
    import json

    # Multiple statements on one line
    y = 1
    z = 2

    return x


def another_bad_function(
    param1, param2, param3, param4, param5, param6, param7, param8
):
    # Too many arguments
    pass


if __name__ == "__main__":
    result = bad_function()
    print(result)
