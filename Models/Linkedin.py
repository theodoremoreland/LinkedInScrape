import pg8000
from config import (user, password, host, port)


class LinkedIn:

    def __init__(self):
        pass

    def connect(self):
        global connection
        global cursor

        connection = pg8000.connect(user=user,
                                    password=password,
                                    host=host,
                                    port=int(port),
                                    database="linkedin")

        cursor = connection.cursor()

        # Print PostgreSQL version
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")

    def createTables(self):
        cursor.execute('BEGIN TRANSACTION;')
        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS profile (
                            company_id SERIAL PRIMARY KEY,
                            name VARCHAR(25) UNIQUE,
                            followers INTEGER,
                            employees_on_linkedin INTEGER,
                            size INTEGER,
                            URL VARCHAR(100) UNIQUE
                            );
                        ''')

        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS posts (
                            id SERIAL PRIMARY KEY,
                            likes INTEGER,
                            comments INTEGER,
                            date VARCHAR(20),
                            company_id INTEGER REFERENCES profile(company_id)
                            );
                        ''')
        cursor.execute('COMMIT;')

    def intoProfile(self, name, followers, employees_on_linkedin, size, url):
        s = f"INSERT INTO profile(name, followers, employees_on_linkedin, size, url) VALUES ('{name}', {followers}, {employees_on_linkedin}, {size}, '{url}');"
        cursor.execute('BEGIN TRANSACTION;')
        cursor.execute(s)
        cursor.execute('COMMIT;')

    def intoPosts(self, likes, comments, date, company_id):
        s = f"INSERT INTO posts(likes, comments, date, company_id) VALUES ({likes}, {comments}, '{date}', {company_id});"
        cursor.execute('BEGIN TRANSACTION;')
        cursor.execute(s)
        cursor.execute('COMMIT;')

    def select(self):
        cursor.execute("SELECT * from profile;")
        record = cursor.fetchall()
        print(record)
        cursor.execute("SELECT * from posts;")
        record = cursor.fetchall()
        print(record)


linkedIn = LinkedIn()
linkedIn.connect()
linkedIn.createTables()
linkedIn.intoProfile('nrm', 12, 15, 16, '.coym')
linkedIn.intoPosts(3, 8, "march", 1)
linkedIn.select()
