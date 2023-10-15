import datetime
import unittest
from unittest.mock import patch
from src.controllers.auth import Login


class testLogin(unittest.TestCase):
    def test_login_success(self):
        return_value = [1, 1]
        username = "naugs"
        password = "1234"
        auth = Login()
        response = auth.login_user(username, password)
        self.assertEqual(response, return_value)

    def test_login_failure(self):
        return_value = None
        username = "naugs"
        password = "12345"
        auth = Login()
        response = auth.login_user(username, password)
        self.assertEqual(response, return_value)

    @patch("src.controllers.auth.db")
    def test_sign_up_success(self, mock_db_object):
        return_value = None
        mock_db_object.return_value = return_value
        name = "Aaryan"
        email = "naugs@mail.com"
        username = "naugs"
        passwrord = "1234"
        login = Login()
        response = login.sign_up(name, email, username, passwrord)
        self.assertEqual(response, return_value)

    @patch("src.controllers.auth.db")
    def test_validate_credential_failure(self, mock_db_object):
        return_value = None
        mock_db_object.return_value = return_value
        username = "naugs"
        plain_password = "1234"
        auth = Login()
        response = auth.validate_credentials(username=username, password=plain_password)
        self.assertEqual(response, return_value)

    @patch("src.controllers.auth.db")
    def test_validate_credentials_success(self, mock_db_object):
        return_value = [
            (
                2,
                "naugs",
                "03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4",
                1,
                datetime.datetime(2023, 9, 9, 20, 37, 2),
            )
        ]
        mock_db_object.get_from_db.return_value = return_value
        username = "naugs"
        plain_password = "1234"
        auth = Login()
        response = auth.validate_credentials(username=username, password=plain_password)
        self.assertEqual(response, [return_value[0][2], return_value[0][3]])

    @patch("src.controllers.auth.db")
    def test_get_role_success(self, mocked_db_object):
        return_value = [(2, 1, 1)]
        mocked_db_object.get_from_db.return_value = return_value
        login = Login()
        user_id = 1
        response = login.get_role(user_id)
        self.assertEqual([return_value[0][2], user_id], response)

    # @patch(
    #     "src.controllers.auth.db",
    #     return_value=[(1, "John Doe", 4)],
    # )
    # @patch("src.controllers.auth.db")
    # def test_update_role_success(self, mock_update_db, mock_get_from_db):
    #     login = Login()
    #     user_id = 1
    #     login.update_role(user_id)

    #     mock_get_from_db.assert_called_once_with(
    #         "SELECT * FROM user_roles where uid = %s", (user_id,)
    #     )
    #     mock_update_db.assert_called_once_with(
    #         "UPDATE user_roles SET role_id = %s WHERE uid = %s", (2, user_id)
    #     )

    # @patch("src.controllers.auth.db.get_from_db")
    # @patch("src.controllers.auth.db.update_db")
    # def test_update_role_success(self, mocked_get_from_db, mocked_update_db):
    #     mocked_get_from_db.return_value = [(2, 1, 1)]
    #     login = Login()
    #     user_id = 1
    #     respone = Login.update_role(user_id)
    #     mocked_update_db.return_value = None
    #     # mocked_get_from_db.assert_called_once_with(
    #     #     "SELECT * FROM user_roles where uid = %s", (user_id,)
    #     # )
    #     # mocked_update_db.assert_called_once_with(
    #     #     "UPDATE user_roles SET role_id = %s WHERE uid = %s", (2, user_id)
    #     # )

    #     self.assertEqual(respone, None)
