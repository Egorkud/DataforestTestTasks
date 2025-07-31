from db.database import Database

db = Database()
db.insert_product(
    name='Test Product',
    category='DevOps',
    price_range='500$-700$',
    description='Test Product Description'
)
print("Product inserted successfully")
db.close()
