# Third party
import pg8000

# Custom
from .database_cred import user, password, host, port


class DB:
    def __init__(self):
        pass

    def connect(self):
        global connection
        global cursor

        connection = pg8000.connect(
            user=user, password=password, host=host, port=int(port), database="web_data"
        )

        cursor = connection.cursor()

        # Print PostgreSQL version
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")

    def create_table_company_profiles(self):
        cursor.execute("BEGIN TRANSACTION;")
        cursor.execute(
            """
                        CREATE TABLE IF NOT EXISTS company_profiles (
                            company_id SERIAL PRIMARY KEY,
                            name TEXT,
                            followers INTEGER,
                            employees_on_linkedin INTEGER,
                            URL TEXT
                            );
                        """
        )
        cursor.execute("COMMIT;")

    def create_table_company_posts(self):
        cursor.execute("BEGIN TRANSACTION;")
        cursor.execute(
            """
                        CREATE TABLE IF NOT EXISTS company_posts (
                            id SERIAL PRIMARY KEY,
                            content TEXT,
                            likes INTEGER,
                            comments INTEGER,
                            date VARCHAR(20),
                            company_id INTEGER REFERENCES company_profiles(company_id)
                            );
                        """
        )
        cursor.execute("COMMIT;")

    def into_company_profiles(self, name, followers, employees_on_linkedin, url):
        s = f"INSERT INTO company_profiles(name, followers, employees_on_linkedin, url) VALUES ('{name}', {followers}, {employees_on_linkedin}, '{url}');"
        cursor.execute("BEGIN TRANSACTION;")
        cursor.execute(s)
        cursor.execute("COMMIT;")

    def into_company_posts(self, content, likes, comments, date, company_id):
        s = f"INSERT INTO company_posts(content, likes, comments, date, company_id) VALUES ('{content}', {likes}, {comments}, '{date}', {company_id});"
        cursor.execute("BEGIN TRANSACTION;")
        cursor.execute(s)
        cursor.execute("COMMIT;")

    def select(self):
        try:
            cursor.execute("SELECT * from company_profiles;")
            record = cursor.fetchall()
            print(record)
        except Exception as e:
            pass
        try:
            cursor.execute("SELECT * from company_posts;")
            record = cursor.fetchall()
            print(record)
        except Exception as e:
            pass
