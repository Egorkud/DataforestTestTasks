import threading

from config import Config
from db.database import Database
from vendr_web import VendrWebScraper
from workers import product_queue, result_queue
from workers import worker_saver, worker_scraper

if __name__ == "__main__":
    vendr_scraper = VendrWebScraper()
    database = Database()
    categories = Config.SCRAPE_CATEGORIES

    # Потік збереження даних
    saver_thread = threading.Thread(target=worker_saver)
    saver_thread.start()

    threads = []
    for category in categories:
        category_url = f"/categories/{category}"
        category_data = vendr_scraper.get_data_from_url(category_url)
        subcategories_urls = vendr_scraper.get_subcategories_urls(category_data)
        subcategory_products_urls = vendr_scraper.get_subcategory_product_urls(subcategories_urls)

        for url in subcategory_products_urls:
            product_queue.put(url)

    # Старт парсерів
    for _ in range(Config.MAX_WORKER_THREADS):
        t = threading.Thread(target=worker_scraper)
        t.start()
        threads.append(t)

    # Сигнали завершення парсерів
    for _ in range(Config.MAX_WORKER_THREADS):
        product_queue.put("STOP")

    # Очікування завершення парсерів
    for t in threads:
        t.join()

    # Сигнал завершення для saver
    result_queue.put("STOP")

    # Очікування завершення saver
    saver_thread.join()
