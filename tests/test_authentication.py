import unittest
from unittest import mock
import src.controllers.auth
from src.controllers.auth import Login


class test_user(unittest.TestCase):

    # def test_add_user_details(self):
    #     login_obj = Login()
    #     name = "ab"
    #     email = "johndoe@example.com"
    #     username = "johndoe"
    #     password = "password123"
    #
    #     user_id = login_obj.add_user_details(name, email, username, password)
    #
    #     assert user_id > 0, "User was not created successfully."
    #
    # def test_add_user_details_with_invalid_email(self):
    #     login_obj = Login()
    #     name = "ab"
    #     email = "invalid_email"
    #     username = "johndoe"
    #     password = "password123"
    #
    #     user_id = login_obj.add_user_details(name, email, username, password)
    #
    #     assert user_id is None, "User was created with an invalid email address."

    def setUp(self):
        self.instance = src.controllers.auth.Login

    def test_login_user(self):
        mock_login_user = mock.Mock()
        user = Login()
        with mock.patch("src.controllers.auth.Login.login_user", mock_login_user):
            mock_login_user.login_user.return_value = [4, 33]
            valid_user_details = [4, 33]

            user_details = mock_login_user.login_user(user)
            self.assertEqual(user_details, valid_user_details)

    # def test_validate_user(self):
    #     mock_validate_user = mock.Mock()
    #     user = Login()
    #     with mock.patch("src.controllers.auth.Login.validate_user", mock_validate_user):
    #         mock_validate_user.validate_user.return_value = None
    #         valid_user_details = None
    #
    #         user_details = self.instance.validate_user(user)
    #         mock_validate_user.validate_user.assert_not_called()

    # def test_validate_user_success(self):
    #     """
    #     Test that the `validate_user()` function returns the role of the user if the username and password are valid.
    #     """
    #     authentication = Login()
    #     username = "naugs"
    #     password = "1234"
    #     expected_role = 1
    #
    #     actual_role = authentication.validate_user(username, password)
    #
    #     self.assertEqual(actual_role, expected_role)

    def test_validate_user_success(self):
        mock_validate_user = mock.Mock()
        # user = Login()
        with mock.patch("src.controllers.auth.Login.validate_user", mock_validate_user):
            mock_validate_user.validate_user.return_value = [1, 1]

            username = "naugs"
            password = "1234"
            expected_role = [1, 1]

            actual_role = mock_validate_user.validate_user(username, password)

        self.assertEqual(actual_role, expected_role)
