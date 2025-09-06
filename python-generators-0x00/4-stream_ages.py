import mysql.connector

def stream_user_ages():
    """
    Generator that yields user ages one by one from user_data.
    """
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="RootPass123!",
        database="ALX_prodev"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")  # Only ages needed

    for row in cursor:  # 1st loop
        yield int(row["age"])

    cursor.close()
    conn.close()


def compute_average_age():
    """
    Computes the average age of users using the generator.
    """
    total = 0
    count = 0
    for age in stream_user_ages():  # 2nd loop
        total += age
        count += 1

    if count == 0:
        return 0
    return total / count


# Main script
if __name__ == "__main__":
    average_age = compute_average_age()
    print(f"Average age of users: {average_age}")
