import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator to fetch rows from user_data table in batches.
    """
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="RootPass123!",
        database="ALX_prodev"
    )
    cursor = conn.cursor(dictionary=True)
    offset = 0

    while True:
        cursor.execute(
            "SELECT user_id, name, email, age FROM user_data LIMIT %s OFFSET %s",
            (batch_size, offset)
        )
        batch = cursor.fetchall()
        if not batch:
            break
        yield batch
        offset += batch_size

    cursor.close()
    conn.close()


def batch_processing(batch_size):
    """
    Returns a generator that processes each batch to filter users over age 25.
    """
    def generator():
        for batch in stream_users_in_batches(batch_size):
            filtered = [user for user in batch if int(user["age"]) > 25]
            yield filtered

    return generator()  # <- now we return the generator


# Example usage
if __name__ == "__main__":
    for processed_batch in batch_processing(batch_size=3):
        print("Processed batch:")
        for user in processed_batch:
            print(user)
