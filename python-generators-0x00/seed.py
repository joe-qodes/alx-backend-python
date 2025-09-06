import csv
import uuid
import mysql.connector
from mysql.connector import errorcode


# 1. Connect to MySQL server

def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",        # change if needed
            password="RootPass123!" # change if needed
        )
        print(" Connected to MySQL server.")
        return connection
    except mysql.connector.Error as err:
        print(f" Error: {err}")
        return None


# 2. Create database if not exists

def create_database(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print(" Database ALX_prodev is ready.")
    except mysql.connector.Error as err:
        print(f" Failed creating database: {err}")
    finally:
        cursor.close()

# 3. Connect to ALX_prodev DB

def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",        # change if needed
            password="RootPass123!",# change if needed
            database="ALX_prodev"
        )
        print(" Connected to ALX_prodev database.")
        return connection
    except mysql.connector.Error as err:
        print(f" Error: {err}")
        return None

# 4. Create user_data table

def create_table(connection):
    cursor = connection.cursor()
    table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        age DECIMAL(3,0) NOT NULL,
        INDEX idx_email (email)
    )
    """
    try:
        cursor.execute(table_query)
        print(" Table user_data is ready.")
    except mysql.connector.Error as err:
        print(f" Failed creating table: {err}")
    finally:
        cursor.close()


# 5. Insert data from CSV

def insert_data(connection, data):
    cursor = connection.cursor()
    insert_query = """
    INSERT IGNORE INTO user_data (user_id, name, email, age)
    VALUES (%s, %s, %s, %s)
    """
    try:
        cursor.executemany(insert_query, data)
        connection.commit()
        print(f" Inserted {cursor.rowcount} rows into user_data.")
    except mysql.connector.Error as err:
        print(f" Error inserting data: {err}")
    finally:
        cursor.close()


# 6. Main script

if __name__ == "__main__":
    # Step 1: Connect to MySQL server
    root_conn = connect_db()
    if root_conn:
        create_database(root_conn)
        root_conn.close()

    # Step 2: Connect to ALX_prodev DB
    prodev_conn = connect_to_prodev()
    if prodev_conn:
        create_table(prodev_conn)

        # Load CSV and prepare data
        data = []
        with open("user_data.csv", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append((
                    str(uuid.uuid4()), # Generate UUID for user_id
                    row["name"].strip(),
                    row["email"].strip(),
                    row["age"].strip()
                ))

        # Insert data into DB
        insert_data(prodev_conn, data)
        prodev_conn.close()
