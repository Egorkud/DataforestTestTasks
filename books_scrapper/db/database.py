import json

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
        # Or make connection to another table from product_info (better normalisation possible)
        create_query = """
                       CREATE TABLE IF NOT EXISTS books
                       (
                           id                 SERIAL PRIMARY KEY,
                           title              TEXT NOT NULL,
                           category           TEXT NOT NULL,
                           price              TEXT,
                           rating             TEXT,
                           stock_availability TEXT,
                           image_url          TEXT,
                           description        TEXT,
                           product_info       JSONB
                       ); \
                       """
        self.cursor.execute(create_query)

    def insert_product(self, title: str, category: str, price: float, rating: str, stock_availability: str,
                       image_url: str, description: str, product_info: dict) -> None:
        insert_query = """
                       INSERT INTO books(title, category, price, rating, stock_availability, image_url,
                                         description, product_info)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                       """
        self.cursor.execute(insert_query,
                            (title, category, price, rating, stock_availability, image_url, description,
                             json.dumps(product_info)))

    def close(self):
        self.cursor.close()
        self.conn.close()
