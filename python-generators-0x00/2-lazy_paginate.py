import mysql.connector

def paginate_users(page_size, offset):
    """
    Fetch a single page of users from the database starting at the given offset.
    """
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="RootPass123!",
        database="ALX_prodev"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT user_id, name, email, age FROM user_data LIMIT %s OFFSET %s",
        (page_size, offset)
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def lazy_paginate(page_size):
    """
    Generator that lazily loads pages from user_data.
    """
    offset = 0
    while True:  # Only 1 loop
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size


# Example usage
if __name__ == "__main__":
    for page in lazy_paginate(page_size=3):
        print("New page:")
        for user in page:
            print(user)
