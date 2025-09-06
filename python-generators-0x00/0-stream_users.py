# 0-stream_users.py
import mysql.connector

def stream_users():
    """
    Generator to fetch rows one by one from the user_data table.
    """
    # Connect to the database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="RootPass123!",
        database="ALX_prodev"
    )
    cursor = conn.cursor(dictionary=True)  # fetch rows as dictionaries

    cursor.execute("SELECT user_id, name, email, age FROM user_data")

    # Yield one row at a time
    for row in cursor:  # Only 1 loop
        yield row

    # Clean up
    cursor.close()
    conn.close()


# Example usage
if __name__ == "__main__":
    for user in stream_users():
        print(user)
