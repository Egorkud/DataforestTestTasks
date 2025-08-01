from config import Config
from vendr_web import VendrWebScraper

if __name__ == "__main__":
    vendr_scraper = VendrWebScraper()
    categories = Config.SCRAPE_CATEGORIES

    for category in categories:
        category_data = vendr_scraper.get_category_data(category)
        subcategories = vendr_scraper.get_subcategories_urls(category_data)
        print(subcategories)