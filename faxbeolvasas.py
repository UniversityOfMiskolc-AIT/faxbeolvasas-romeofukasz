# -*- coding: utf-8 -*-

"""Fax reader for bank account numbers

Created by Romeo Ervin Fukasz (FY78UY).
"""

import sys
import argparse


def checksum(account_number):
    """Calculates the checksum of the input bank account and validates it.

    Keyword arguments:
    account_number -- The digits of the bank account in a list of integers
    """

    if not isinstance(account_number, list) or not all([isinstance(element, int) for element in account_number]):
        raise TypeError("The input of the checksum function should be a list of integers")

    if len(account_number) != 9:
        raise ValueError("The input list should have 9 digits")

    multiplied_digits = [element * (index + 1) for index, element in enumerate(account_number)]
    return sum(multiplied_digits) % 11


def generate_account_line(account_number):
    """Generates a string with the account number and its status.
    The status is ERR if the checksum is not 0.
    The status is ILL if not all digits are valid.
    In other cases there is no status displayed.

    Keyword arguments:
    account_number -- The digits of the bank account in a list of integers
    """
    if not isinstance(account_number, list) or not all([isinstance(element, int) for element in account_number]):
        raise TypeError("The input of the checksum function should be a list of integers")

    if len(account_number) != 9:
        raise ValueError("The input list should have 9 digits")

    status = ""
    is_illegal_number = any([element < 0 for element in account_number])

    if is_illegal_number:
        status = " ILL"

        for index, element in enumerate(account_number):
            if element < 0:
                account_number[index] = "?"

    elif checksum(account_number) != 0:
        status = " ERR"

    account_number_string = "".join([str(digit) for digit in account_number])

    return f"{account_number_string}{status}"


def parse_account(input_text):
    """Parses an account from an entry of read fax data. (3 data lines)

    Keyword arguments:
    input_text -- list of three lines that represent a bank account data in the input file
    """

    if not isinstance(input_text, list) or not all([isinstance(element, str) for element in input_text]):
        raise TypeError("The input of parse_account must be a list of three strings")

    if any(len(line) != 27 for line in input_text):
        raise ValueError("Each line must be exactly 27 characters")

    digits_as_fax_matrices = {  # each digit represented as a 3x3 matrix of characters
        1: ["   ", "  |", "  |"],
        2: [" _ ", " _|", "|_ "],
        3: [" _ ", " _|", " _|"],
        4: ["   ", "|_|", "  |"],
        5: [" _ ", "|_ ", " _|"],
        6: [" _ ", "|_ ", "|_|"],
        7: [" _ ", "  |", "  |"],
        8: [" _ ", "|_|", "|_|"],
        9: [" _ ", "|_|", " _|"],
        0: [" _ ", "| |", "|_|"],
    }

    result = []

    for i in range(0, 27, 3):
        digit_reading = [input_text[0][i:i+3], input_text[1][i:i+3], input_text[2][i:i+3]]

        if digit_reading not in digits_as_fax_matrices.values():
            result.append(-1)
        else:  # search for the digit if the reading is valid
            for digit, reading in digits_as_fax_matrices.items():
                if digit_reading == reading:
                    result.append(digit)

    return result


def parse_input_file(file_name):
    """Parses the data from the specified input file.

    Keyword arguments:
    file_name -- the path of the input file
    """

    data = ""

    with open(file_name, "r") as f:
        data = f.read()

    valid_characters = {' ', '_', '|', }
    data_lines = data.splitlines()
    every_fourth_line = data_lines[3::4]
    del data_lines[3::4]  # remove every empty line from data lines

    every_data_line_use_valid_characters = all([set(line).issubset(valid_characters) for line in data_lines])
    every_data_line_is_27_in_length = all([len(line) == 27 for line in data_lines])
    every_fourth_line_is_empty = all(set(line).issubset({' '}) for line in every_fourth_line)

    if not (every_data_line_use_valid_characters and every_data_line_is_27_in_length and every_fourth_line_is_empty):
        raise ValueError("The input data is not valid")

    account_numbers = []

    for i in range(0, len(data_lines), 3):
        fax_reading_data = data_lines[i:i+3]
        account_numbers.append(parse_account(fax_reading_data))

    return account_numbers


def write_output_file(file_name, account_numbers):
    """Generates account lines and writes them to the specified output file.

    Keyword arguments:
    file_name -- the path of the output file
    account_numbers -- the account number digits data in a list of integer lists
    """

    account_lines = [generate_account_line(account_number) for account_number in account_numbers]

    with open(file_name, "w") as f:
        f.write('\n'.join(account_lines))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reads bank account data from fax text file")
    parser.add_argument("--input", dest="input_file_path", type=str, nargs='?', default="input.txt",
                        help="The path of the input file")
    parser.add_argument("--output", dest="output_file_path", type=str, nargs='?', default="output.txt",
                        help="The path of the output file")
    args = parser.parse_args()

    try:
        account_numbers = parse_input_file(file_name=args.input_file_path)
        write_output_file(args.output_file_path, account_numbers)
    except Exception as e:
        print(f"An error occured: {e} {type(e)}", file=sys.stderr)
