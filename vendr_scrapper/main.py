from config import Config
from vendr_web import VendrWebScraper

if __name__ == "__main__":
    vendr_scraper = VendrWebScraper()
    categories = Config.SCRAPE_CATEGORIES

    # TODO: add get data from each product
    # TODO: add multithreading scrapping
    # TODO: add multithreading one thread save to DB
    for category in categories:
        category_url = f"/categories/{category}"
        category_data = vendr_scraper.get_data_from_url(category_url)
        subcategories_urls = vendr_scraper.get_subcategories_urls(category_data)
        subcategory_products_urls = vendr_scraper.get_subcategory_product_urls(subcategories_urls)
        products_data = vendr_scraper.get_product_data(subcategory_products_urls)

        # TEST check scraped data
        with open("subcategories_urls.txt", "a") as file:
            file.write("\n".join(subcategories_urls))

        with open("subcategory_products_urls.txt", "a") as file:
            file.write("\n".join(subcategory_products_urls))