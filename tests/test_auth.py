import hashlib
import sys
import unittest
from io import StringIO
from unittest import mock
from unittest.mock import patch, MagicMock
from src.controllers.auth import Login, input_choice


class testLogin(unittest.TestCase):

    @patch('builtins.input', return_value='1')
    def test_login_menu_sign_up(self, mock_input):
        login_menu = Login()
        result = login_menu.login_menu()
        self.assertEqual(result, [None, None])

    @patch('builtins.input', return_value='2')
    def test_login_menu_login(self, mock_input):
        login_menu = Login()
        login_menu.login_user = MagicMock(return_value=["user", 1])
        result = login_menu.login_menu()
        self.assertEqual(result, ["user", 1])

    @patch("src.controllers.auth.DatabaseConnection.get_from_db")
    def test_validate_user(self, mock_get_from_db):
        username = "naugs"
        plain_password = "1234"
        hashed_password = hashlib.sha256(plain_password.encode('utf-8')).hexdigest()
        mock_get_from_db.return_value = [(1, username, hashed_password, "user")]
        auth = Login()
        with unittest.mock.patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            role = auth.validate_user(username, plain_password)
        sys.stdout = sys.__stdout__
        printed_output = mock_stdout.getvalue().strip()
        self.assertEqual(role, [hashed_password, "user"])
        self.assertIn("You logged into the system successfully.", printed_output)

    @patch('src.controllers.auth.DatabaseConnection.get_from_db', return_value=[(1, 'John Doe', 2)])
    def test_get_role_success(self, mock_get_from_db):
        login = Login()
        user_id = 1
        role = login.get_role(user_id)

        mock_get_from_db.assert_called_once_with('SELECT * FROM user_roles where uid = %s', (user_id,))
        self.assertEqual(role, [2, user_id])

    @patch('src.controllers.auth.DatabaseConnection.get_from_db', return_value=[(1, 'John Doe', 4)])
    @patch('src.controllers.auth.DatabaseConnection.update_db')
    def test_update_role_success(self, mock_update_db, mock_get_from_db):
        login = Login()
        user_id = 1
        login.update_role(user_id)

        mock_get_from_db.assert_called_once_with('SELECT * FROM user_roles where uid = %s', (user_id,))
        mock_update_db.assert_called_once_with('UPDATE user_roles SET role_id = %s WHERE uid = %s', (2, user_id))

    @patch('builtins.input', return_value='1')
    def test_input_choice_valid(self, mock_input):
        result = input_choice()
        self.assertEqual(result, 1)
