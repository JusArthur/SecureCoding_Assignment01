import os
import pymysql
from urllib.request import urlopen

db_config = {
    # Not hard-coded credentials
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'database': os.environ.get('DB_NAME', 'test')
}

def get_user_input():
    # use validation for input
    user_input = input('Enter your name: ').strip()
    if not re.match(r'^[A-Za-z\s]{1,50}$', user_input):
        print("Invalid input.")
        return None
    return user_input

def send_email(to, subject, body):
    # prevent dangerous command
    safe_body = body.replace('"', '\\"').replace("'", "\\'")
    safe_subject = subject.replace('"', '\\"').replace("'", "\\'")
    safe_to = to.replace('"', '\\"').replace("'", "\\'")
    os.system(f'echo "{safe_body}" | mail -s "{safe_subject}" "{safe_to}"')

def get_data():
    # use https and detect the content
    url = 'https://secure-api.example.com/get-data'
    try:
        data = urlopen(url, timeout=5).read().decode()
        if len(data) > 1000:
            print("Data too large, truncated.")
            data = data[:1000]
        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def save_to_db(data):
    if not data:
        print("No data to save.")
        return
    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()
        # use params to improve SQL and protect it from injection
        query = "INSERT INTO mytable (column1, column2) VALUES (%s, %s)"
        cursor.execute(query, (data, 'Another Value'))
        connection.commit()
    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    user_input = get_user_input()
    data = get_data()
    save_to_db(data)
    send_email('admin@example.com', 'User Input', user_input)
