import unittest
from unittest.mock import patch
from src.helpers.inputs_and_validations import validate_username, validate_name, validate_email, validate_password, \
    get_string_input, get_float_input, input_name, input_user_name


class TestInputsandValidations(unittest.TestCase):

    def test_valid_username(self):
        username = "ValidUsername123"
        result = validate_username(username)
        self.assertIsNotNone(result)

    def test_invalid_username_special_characters(self):
        username = "Invalid@Username"
        result = validate_username(username)
        self.assertIsNone(result)

    def test_invalid_username_whitespace(self):
        username = "Invalid Username"
        result = validate_username(username)
        self.assertIsNone(result)

    def test_invalid_username_empty_string(self):
        username = ""
        result = validate_username(username)
        self.assertIsNone(result)

    def test_valid_name(self):
        name = "John Doe"
        result = validate_name(name)
        self.assertIsNotNone(result)

    @patch('builtins.input', side_effect=['user@example.com'])
    def test_valid_email(self, mock_input):
        email = 'user@example.com'
        result = validate_email(email)
        self.assertTrue(result)

    @patch('builtins.input', side_effect=['invalid_email', 'user@example.com'])
    def test_invalid_email_then_valid_email(self, mock_input):
        email = 'invalid_email'
        result = validate_email(email)
        self.assertTrue(result)

    @patch('maskpass.askpass', side_effect=['Password1'])
    def test_valid_password(self, mock_askpass):
        password = 'Password1'
        result = validate_password(password)
        self.assertTrue(result)

    @patch('maskpass.askpass', side_effect=['invalid_password', 'Password1'])
    def test_invalid_password_then_valid_password(self, mock_askpass):
        password = 'invalid_password'
        result = validate_password(password)
        self.assertTrue(result)

    @patch('builtins.input', side_effect=['Valid Input'])
    def test_valid_input(self, mock_input):
        message = 'Enter input: '
        result = get_string_input(message)
        self.assertEqual(result, 'Valid Input')

    @patch('builtins.input', side_effect=['', '', 'Non-empty Input'])
    def test_empty_input_then_valid_input(self, mock_input):
        message = 'Enter input: '
        result = get_string_input(message)
        self.assertEqual(result, 'Non-empty Input')

    @patch('builtins.input', side_effect=['5.0'])
    def test_valid_float_input(self, mock_input):
        message = 'Enter a positive number: '
        result = get_float_input(message)
        self.assertEqual(result, 5.0)

    @patch('builtins.input', side_effect=["", " ", "123", "John Doe"])
    def test_input_name(self, mock_input):
        input_name(self)
        self.assertEqual(mock_input.call_count, 4)

    @patch('builtins.input', side_effect=["", "user1", "user_123", "JohnDoe"])
    def test_input_user_name(self, mock_input):
        input_user_name(self)

        self.assertEqual(mock_input.call_count, 4)
