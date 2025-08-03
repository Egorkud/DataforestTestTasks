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

    def insert_product(self, item):
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                            INSERT INTO products (name, category, subcategory, price_low, price_high, price_median,
                                                  description)
                            VALUES (%s, %s, %s, %s, %s, %s, %s); \
                            """,
                            (item['name'], item['category'], item['subcategory'], float(item['price_low']),
                             float(item['price_high']), float(item['price_median']), item['description']))
            self.conn.commit()
        except Exception as e:
            print(f"DB insert error: {e}")

    def close(self):
        self.cursor.close()
        self.conn.close()
