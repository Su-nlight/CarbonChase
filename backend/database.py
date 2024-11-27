import os
from mysql.connector import pooling, Error

# Connection pool for efficient database connection management
connection_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,  # Adjust based on your load
    pool_reset_session=True,
    host='127.0.0.1',  # Replace with your MySQL host
    database='carbonchase',  # Replace with your database name
    user='asydel',  # Replace with your MySQL username
    password= "fafdajalebi"  # Replace with your MySQL password
)


class Database:
    @staticmethod
    def execute_query(query: str, params: tuple):
        """Executes a given SQL query using a connection from the pool."""
        try:
            # Get connection from the pool
            connection = connection_pool.get_connection()
            if connection.is_connected():
                cursor = connection.cursor(buffered=True)
                cursor.execute(query, params)
                connection.commit()
                return cursor.rowcount  # Optionally    return the number of rows affected
        except Error as e:
            raise RuntimeError(f"Database error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def get_user_data(username:str, required_fields:tuple):
        try:
            connection = connection_pool.get_connection()
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(f"SELECT {', '.join(required_fields)} FROM user_data WHERE username = '{username}'")
                value=cursor.fetchone()
                req_data={}
                for i in range(len(required_fields)):
                    req_data[required_fields[i]] = value[i]
                return req_data.copy()

        except Error as e:
            raise RuntimeError(f"Database error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def get_user_pass(username: str):
        try:
            connection = connection_pool.get_connection()
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(f"SELECT hashed_password FROM Users WHERE username = '{username}'")
                value = cursor.fetchone()[0]
                return value

        except Error as e:
            raise RuntimeError(f"Database error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def check_user(username: str, usr_email: str):
        try:
            connection = connection_pool.get_connection()
            if connection.is_connected():
                cursor = connection.cursor(buffered=True)
                cursor.execute(f"SELECT username FROM users WHERE username = '{username}'")
                cursor.execute(f"SELECT email FROM users WHERE email = '{usr_email}'")
                value = cursor.fetchone()
                print(value)
                return value

        except Error as e:
            raise RuntimeError(f"Database error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

def chk_username(username: str):
    try:
        connection = connection_pool.get_connection()
        if connection.is_connected():
            cursor = connection.cursor(buffered=True)
            cursor.execute(f"SELECT username FROM user_data WHERE username = '{username}'")
            value = cursor.fetchone()
            return value

    except Error as e:
        raise RuntimeError(f"Database error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_total_user_data(username:str):
    try:
        connection = connection_pool.get_connection()
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(f"select users.email, user_data.* from users inner join user_data on users.username=user_data.username where users.username='{username}';")
            value=cursor.fetchone()
            return value
    except Error as e:
        raise RuntimeError(f"Database error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
