import datetime
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
        print("Welcome to login. Please enter your crendentials")
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
                
    @classmethod
    def create_account(cls):
        """Creates a new user"""
        cls.conn = get_db_connection()
        print("Welcome to Account Creation. Please enter your crendentials below")
        print("Please enter first name:")
        

        first_name = input("Please enter first name: ").strip()
        last_name = input("Please enter last name: ").strip()
        email = input("Please enter your email: ").strip()
        platform = input("Please enter the gaming platform you own: ").strip()

        while True:
            username = input("Please enter a new username: ").strip()
            if cls.is_username_taken(username) != -1:
                print("Username already taken - please enter a different one.")
            else:
                break

        while True:
            password = input("Please enter a new password: ").strip()
            if len(password) < 6:
                print("Password must be at least 6 characters long.")
            else:
                break

        current_time = datetime.datetime.now()

        try:
            with cls.conn.cursor() as cursor:
                increment_user_id = cls.increment_counter_user_id()
                cursor.execute("""
                    INSERT INTO users (userID, username, email, password, first_name, last_name, platform, created_at, last_login)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NULL)
                """, (increment_user_id, username, email, password, first_name, last_name, platform, current_time))
                cls.conn.commit()
                print("✅ Your account has been created! Please sign in to access other functionalities.")
        except psycopg2.Error as e:
            print(f"❌ Database error: {e}")
            cls.conn.rollback()



    
    @staticmethod
    def print_begin_menu():
        print("\nWelcome to the Video Game!")
        print("Please sign in or create account with the folloeing commands: ")
        print("1: Create Account")
        print("0: Login")
        print("9: Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            User.create_account()
        elif choice == "0":
            User.login()
        elif choice == "9":
            print("Exiting application.")
            exit()
        else:
            print("Invalid option. Try again.")
            User.print_begin_menu()







# Function to reconnect to the database
def reconnect_db():
    print("Attempting to reconnect to the database...")
    conn = get_db_connection()
    if conn:
        print("Reconnected to the database successfully.")
    return conn