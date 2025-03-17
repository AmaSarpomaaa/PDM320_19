import psycopg2
from db import get_db_connection  # Ensure db.py is in the same directory
# AUTHOR : Christabel Osei
conn = get_db_connection()

class User:
    user_id = -1  # Static user ID
    login_checker = False
    conn = None
    session = None

    def __init__(self):
        self.conn = get_db_connection()
        
    @staticmethod
    def is_username_taken(username):
        with User.conn.cursor() as cursor:
            cursor.execute('SELECT "userID" FROM "users" WHERE username = %s', (username,))
            result = cursor.fetchone()
            return result[0] if result else -1
        
    @staticmethod
    def login():
        username = input("Enter username: ")
        password = input("Enter password: ")

        with User.conn.cursor() as cursor:
            cursor.execute('SELECT "userID" FROM "users" WHERE username = %s AND password = %s', 
                       (username, password))
            result = cursor.fetchone()

            if result:
                User.user_id = result[0]
                User.login_checker = True
                print("Login successful!")
            else:
                print("Invalid credentials.")
                
    @staticmethod
    def create_account():
        username = input("Enter desired username: ")
        password = input("Enter password: ")

        if User.is_username_taken(username) != -1:
            print("Username already taken.")
            return

        new_user_id = User.increment_counter_user_id()
        with User.conn.cursor() as cursor:
            cursor.execute('INSERT INTO "users" ("userID", "username", "password") VALUES (%s, %s, %s)',
                       (new_user_id, username, password))
            User.conn.commit()
            print("Account created successfully!")



    








# Function to reconnect to the database
def reconnect_db():
    print("Attempting to reconnect to the database...")
    conn = get_db_connection()
    if conn:
        print("Reconnected to the database successfully.")
    return conn