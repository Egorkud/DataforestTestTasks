from books_scrapper.db.database import Database

db = Database()
db.insert_product(
    title='Test Product',
    category='Test Category',
    price=5.00,
    rating='12+',
    stock_availability='AVAILABLE',
    image_url="url_link",
    description='Test Description',
    product_info={
        "UPC": "qweasd",
        "TAX": "123",
        "Price": "150",
    }
)
print("Product inserted successfully")
db.close()
