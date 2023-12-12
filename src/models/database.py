import os
from dotenv import load_dotenv
import mysql.connector
from typing import Optional
from src.helpers.exceptions import DbException

load_dotenv()


class DatabaseConnection:
    def __init__(self):
        try:
            self.db = mysql.connector.connect(
                host=os.getenv("HOST"),
                user=os.getenv("USER"),
                password=os.getenv("PASSWORD"),
                database=os.getenv("DATABASE"),
                autocommit=True,
            )

            self.cursor = self.db.cursor()
        except Exception:
            raise ValueError

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()

    def insert_into_db(self, query, val):
        try:
            self.cursor.execute(query, val)
            user_id = self.cursor.lastrowid
            return user_id
        except:
            raise DbException

    def update_db(self, query, val):
        try:
            self.cursor.execute(query, val)
            return self.cursor.lastrowid
        except:
            raise DbException

    def delete_from_db(self, query, val):
        try:
            self.cursor.execute(query, val)
        except:
            raise DbException

    def get_from_db(self, query, val=None):
        try:
            if val is None:
                self.cursor.execute(query)
                response = self.cursor.fetchall()
                return response
            else:
                self.cursor.execute(query, val)
            response = self.cursor.fetchall()
            return response
        except:
            raise DbException

    def get_paginated(
        self, query, val=None, page: Optional[int] = None, size: Optional[int] = None
    ):
        try:
            if page is not None and size is not None:
                # Apply pagination
                offset = (page - 1) * size
                query += f" LIMIT {size} OFFSET {offset}"
                self.cursor.execute(query, val)
                response = self.cursor.fetchall()
                total_count = self.get_total_count(query, val)
                return response, total_count
            else:
                # No pagination
                if val is None:
                    self.cursor.execute(query)
                    response = self.cursor.fetchall()
                    return response
                else:
                    self.cursor.execute(query, val)
                    response = self.cursor.fetchall()
                    return response
        except:
            raise DbException

    def get_total_count(self, query, val=None):
        """
        Fetches the total number of rows for a given query.

        Args:
            query (str): The SQL query to execute.
            val (Optional[tuple]): Values to bind to the query. Defaults to None.

        Returns:
            int: The total number of rows.
        """

        count_query = f"SELECT COUNT(*) FROM ({query}) AS subquery"
        self.cursor.execute(count_query, val)
        total_count = self.cursor.fetchone()[0]
        return total_count

    # def get_paginated(
    #     self, query, val=None, page: Optional[int] = None, size: Optional[int] = None
    # ):
    #     try:
    #         if page is not None and size is not None:
    #             # Apply pagination
    #             offset = (page - 1) * size
    #             query += f" LIMIT {size} OFFSET {offset}"
    #             self.cursor.execute(query, val)
    #             response = self.cursor.fetchall()
    #             total_count = self.get_total_count(query, val)
    #             return response, total_count
    #         else:
    #             # No pagination
    #             if val is None:
    #                 self.cursor.execute(query)
    #                 response = self.cursor.fetchall()
    #                 return response
    #             else:
    #                 self.cursor.execute(query, val)
    #                 response = self.cursor.fetchall()
    #                 return response
    #     except:
    #         raise DbException

    # def get_paginated(self, query, val=None, page=None, size=None):
    #     try:
    #         if page is not None and size is not None and val is not None:
    #             # Apply pagination
    #             offset = (page - 1) * size

    #             query += f" LIMIT {size} OFFSET {offset}"
    #             self.cursor.execute(query, val)
    #             response = self.cursor.fetchall()
    #             total_count = self.get_total_count(query, val)
    #             return response, total_count
    #         elif page is not None and size is not None and val is None:
    #             offset = (page - 1) * size
    #             query += f" LIMIT {size} OFFSET {offset}"
    #             self.cursor.execute(query)
    #             response = self.cursor.fetchall()
    #             total_count = self.get_total_count(query, val)
    #             return response, total_count
    #         else:
    #             # No pagination
    #             if val is None:
    #                 self.cursor.execute(query)
    #                 response = self.cursor.fetchall()
    #                 return response
    #             else:
    #                 self.cursor.execute(query, val)
    #                 response = self.cursor.fetchall()
    #                 return response
    #     except:
    #         raise DbException

    # def get_total_count(self, query, val=None):
    #     """
    #     Fetches the total number of rows for a given query.

    #     Args:
    #         query (str): The SQL query to execute.
    #         val (Optional[tuple]): Values to bind to the query. Defaults to None.

    #     Returns:
    #         int: The total number of rows.
    #     """

    #     count_query = f"SELECT COUNT(*) FROM ({query}) AS subquery"
    #     self.cursor.execute(count_query, val)
    #     total_count = self.cursor.fetchone()[0]
    #     return total_count


db = DatabaseConnection()
