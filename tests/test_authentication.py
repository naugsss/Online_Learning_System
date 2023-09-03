import unittest
from unittest.mock import patch, MagicMock
from datetime import date
from src.models.auth import Login
import os
import sys
import unittest
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


# class TestLogin(unittest.TestCase):
#     @patch('src.models.database.DatabaseConnection')
#     def test_add_user_details(self, mock_db_connection):
#         # Create a mock database connection
#         mock_db_instance = mock_db_connection.return_value

#         # Configure the mock to return the expected user_id
#         mock_db_instance.get_role_from_db.return_value = 42

#         # Create a MagicMock object for lastrowid
#         mock_lastrowid = MagicMock()

#         # Mock the lastrowid property of cursor to return the MagicMock
#         mock_cursor = mock_db_instance.__enter__.return_value.cursor.return_value
#         mock_cursor.lastrowid = mock_lastrowid

#         # Create an instance of Login
#         login_instance = Login()

#         # Call the add_user_details method
#         result = login_instance.add_user_details("John Doe", "johndoe@example.com", "johndoe", "password")

#         # Assert that the method returns the expected user_id
#         self.assertEqual(result, mock_lastrowid)

#         # Verify that the database-related methods were called with the expected arguments
#         mock_db_instance.get_role_from_db.assert_called_once_with(
#             "INSERT INTO users (name, email) VALUES (%s, %s)",
#             ("John Doe", "johndoe@example.com"),
#         )
#         mock_db_instance.insert_into_db.assert_any_call(
#             "INSERT INTO user_roles (uid, role_id) VALUES (%s, %s)",
#             (mock_lastrowid, 4),
#         )
#         mock_db_instance.insert_into_db.assert_any_call(
#             "INSERT INTO authentication (username, password, uid, create_at) VALUES (%s, %s, %s, %s)",
#             ("johndoe", 'hashed_password', mock_lastrowid, date.today()),
#         )

# if __name__ == '__main__':
#     unittest.main()

def test_add_user_details():
    """
    Test the add_user_details function.
    """

    login_obj = Login()
    name = "John Doe"
    email = "johndoe@example.com"
    username = "johndoe"
    password = "password123"

    user_id = login_obj.add_user_details(name, email, username, password)

    assert user_id > 0, "User was not created successfully."
    

def test_add_user_details_with_invalid_email():
    """
    Test the add_user_details function with an invalid email address.
    """

    login_obj = Login()
    name = "John Doe"
    email = "invalid_email"
    username = "johndoe"
    password = "password123"

    user_id = login_obj.add_user_details(name, email, username, password)

    assert user_id is None, "User was created with an invalid email address."



