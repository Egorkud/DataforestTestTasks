import psycopg2
from config import Config


class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            dbname=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD
        )
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        create_query = """
                       CREATE TABLE IF NOT EXISTS products
                       (
                           id           SERIAL PRIMARY KEY,
                           name         TEXT  NOT NULL,
                           category     TEXT  NOT NULL,
                           subcategory  TEXT  NOT NULL,
                           price_low    FLOAT NOT NULL,
                           price_high   FLOAT NOT NULL,
                           price_median FLOAT NOT NULL,
                           description  TEXT
                       ); \
                       """
        self.cursor.execute(create_query)

    def insert_product(self, name: str, category: str, price_range: str, description: str):
        insert_query = """
                       INSERT INTO products (name, category, price_range, description)
                       VALUES (%s, %s, %s, %s); \
                       """
        self.cursor.execute(insert_query, (name, category, price_range, description))

    def close(self):
        self.cursor.close()
        self.conn.close()
