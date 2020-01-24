import pg8000
from config import (user, password, host, port)


class Twitter:

    def __init__(self):
        pass

    def connect(self):
        global connection
        global cursor

        connection = pg8000.connect(user=user,
                                    password=password,
                                    host=host,
                                    port=int(port),
                                    database="twitter")

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
                            likes INTEGER,
                            URL VARCHAR(100) UNIQUE
                            );
                        ''')

        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS posts (
                            id SERIAL PRIMARY KEY,
                            likes INTEGER,
                            comments INTEGER,
                            retweets INTEGER,
                            date VARCHAR(20),
                            company_id INTEGER REFERENCES profile(company_id)
                            );
                        ''')
        cursor.execute('COMMIT;')

    def intoProfile(self, name, followers, likes, url):
        s = f"INSERT INTO profile(name, followers, likes, url) VALUES ('{name}', {followers}, {likes}, '{url}');"
        cursor.execute('BEGIN TRANSACTION;')
        cursor.execute(s)
        cursor.execute('COMMIT;')

    def intoPosts(self, likes, comments, retweets, date, company_id):
        s = f"INSERT INTO posts(likes, comments, retweets, date, company_id) VALUES ({likes}, {comments}, {retweets}, '{date}', {company_id});"
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


twitter = Twitter()
twitter.connect()
twitter.createTables()
twitter.intoProfile('n', 15, 16, '.coy')
twitter.intoPosts(3, 8, 7, "march", 1)
twitter.select()
