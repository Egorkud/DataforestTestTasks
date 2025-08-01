from contextlib import contextmanager

from scrapper import BookScraper

# TODO: implement add data to DB
# TODO: implement thread scrapping

if __name__ == "__main__":
    @contextmanager
    def book_scraper_context(headless=True):
        scraper = BookScraper(headless)
        try:
            yield scraper
        finally:
            scraper.close()


    with book_scraper_context(headless=True) as scraper:
        data = scraper.scrape_all_books("https://books.toscrape.com/")
