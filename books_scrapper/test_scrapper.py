from scrapper import BookScraper

# TODO: implement add data to DB
# TODO: implement thread scrapping
# TODO: scrap full website
scraper = BookScraper(headless=False)
url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
data = scraper.get_book_data(url)

from pprint import pprint

pprint(data)
