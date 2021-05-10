import unittest
from unittest.mock import patch, mock_open
from faxbeolvasas import checksum, generate_account_line, parse_account, parse_input_file, write_output_file


class ChecksumTestCase(unittest.TestCase):

    def test_zero_on_valid_account(self):
        self.assertEqual(checksum([4, 5, 7, 5, 0, 8, 1, 0, 0]), 0)

    def test_zero_on_second_valid_account(self):
        self.assertEqual(checksum([0, 1, 1, 2, 0, 0, 7, 0, 9]), 0)

    def test_not_zero_on_invalid_account(self):
        self.assertNotEqual(checksum([1, 2, 3, 4, 5, 6, 7, 8, 9]), 0)

    def test_not_zero_on_second_invalid_account(self):
        self.assertNotEqual(checksum([1, 1, 1, 1, 1, 1, 1, 1, 1]), 0)

    def test_if_invalid_input_raises_value_error(self):
        with self.assertRaises(TypeError):
            checksum(("a", "b", "c"))

    def test_if_wrong_number_of_digits_raises_value_error(self):
        with self.assertRaises(ValueError):
            checksum([1, 2, 3, 4, 5, 6, 7, 8, 9, 0])


class GenerateAccountLineTestCase(unittest.TestCase):

    def test_line_on_valid_account(self):
        self.assertEqual(generate_account_line([4, 5, 7, 5, 0, 8, 1, 0, 0]), "457508100")

    def test_line_on_second_valid_account(self):
        self.assertEqual(generate_account_line([0, 1, 1, 2, 0, 0, 7, 0, 9]), "011200709")

    def test_line_on_invalid_account(self):
        self.assertEqual(generate_account_line([1, 2, 3, 4, 5, 6, 7, 8, 9]), "123456789 ERR")

    def test_line_on_second_invalid_account(self):
        self.assertEqual(generate_account_line([1, 1, 1, 1, 1, 1, 1, 1, 1]), "111111111 ERR")

    def test_line_on_illegal_account(self):
        self.assertEqual(generate_account_line([4, 5, 1, 3, -1, -1, 0, 8, 2]), "4513??082 ILL")

    def test_line_on_second_illegal_account(self):
        self.assertEqual(generate_account_line([-1, -2, -3, -4, -5, -6, -7, -8, -9]), "????????? ILL")

    def test_if_invalid_input_raises_value_error(self):
        with self.assertRaises(TypeError):
            generate_account_line(("a", "b", "c"))

    def test_if_wrong_number_of_digits_raises_value_error(self):
        with self.assertRaises(ValueError):
            generate_account_line([1, 2, 3, 4, 5, 6, 7, 8, 9, 0])


class ParseAccountTestCase(unittest.TestCase):

    def setUp(self):
        self.valid_input = [
            "    _  _  _  _  _     _  _ ",
            "|_||_   ||_ | ||_|  || || |",
            "  | _|  | _||_||_|  ||_||_|",
        ]
        self.second_valid_input = [
            "    _  _     _  _  _  _  _ ",
            "  | _| _||_||_ |_   ||_||_|",
            "  ||_  _|  | _||_|  ||_| _|",

        ]
        self.invalid_input = [
            "    _  _  _  _  _    ",
            "|_||_   ||_ | ||_|  |",
            "  | _|  | _||_||_|  |",
        ]

    def test_parse_account_with_valid_input(self):
        self.assertEqual(parse_account(self.valid_input), [4, 5, 7, 5, 0, 8, 1, 0, 0])

    def test_parse_account_with_second_valid_input(self):
        self.assertEqual(parse_account(self.second_valid_input), [1, 2, 3, 4, 5, 6, 7, 8, 9])

    def test_if_invalid_input_raises_value_error(self):
        with self.assertRaises(ValueError):
            parse_account(self.invalid_input)

    def test_if_invalid_type_of_input_raises_type_error(self):
        with self.assertRaises(TypeError):
            parse_account([5, 6, 8])


class ParseInputFileTestCase(unittest.TestCase):

    def setUp(self):
        self.valid_input_file_path = "test_data/valid_input.txt"
        self.invalid_input_file_path = "test_data/invalid_input.txt"
        self.inexistent_file_path = "does/not/exist.txt"

        self.valid_inputs_expected_output = [
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [4, 5, 7, 5, 0, 8, 1, 0, 0],
            [1, 0, 0, 0, 1, 0, 7, 0, 0],
            [1, -1, 0, 0, -1, 0, -1, 0, 0],
            [0, 1, 0, 1, 0, 0, 7, 0, 0],
            [9, 8, 7, 6, 5, 4, 3, 2, 1],
            [0, 1, 1, 2, 0, 0, 7, 0, 9],
        ]

    def test_valid_input(self):
        self.assertEqual(parse_input_file(self.valid_input_file_path), self.valid_inputs_expected_output)

    def test_if_raises_file_not_found_error_on_invalid_input_path(self):
        with self.assertRaises(FileNotFoundError):
            parse_input_file("does/not/exist.txt")

    def test_if_raises_value_error_on_invalid_input(self):
        with self.assertRaises(ValueError):
            parse_input_file(self.invalid_input_file_path)


class WriteOutputFileTestCase(unittest.TestCase):

    def setUp(self):
        self.mock_file_path = "mock/file/somefile.txt"

        self.valid_input = [
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [4, 5, 7, 5, 0, 8, 1, 0, 0],
            [1, 0, 0, 0, 1, 0, 7, 0, 0],
            [1, -1, 0, 0, -1, 0, -1, 0, 0],
            [0, 1, 0, 1, 0, 0, 7, 0, 0],
            [9, 8, 7, 6, 5, 4, 3, 2, 1],
            [0, 1, 1, 2, 0, 0, 7, 0, 9],
        ]

        self.valid_inputs_expected_output = \
            "123456789 ERR\n" + \
            "457508100\n" + \
            "100010700\n" + \
            "1?00?0?00 ILL\n" + \
            "010100700\n" + \
            "987654321\n" + \
            "011200709"

    def test_write_output_file_writes_to_proper_path(self):
        with patch('faxbeolvasas.open', mock_open()) as mock:
            write_output_file(self.mock_file_path, self.valid_input)
            mock.assert_called_once_with(self.mock_file_path, "w")

    def test_proper_output_on_valid_input(self):
        with patch('faxbeolvasas.open', mock_open()) as mock:
            write_output_file(self.mock_file_path, self.valid_input)
            mock().write.assert_called_once_with(self.valid_inputs_expected_output)


if __name__ == "__main__":
    unittest.main()
