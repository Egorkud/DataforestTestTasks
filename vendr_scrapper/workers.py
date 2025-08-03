import queue
import time

from config import Config
from db.database import Database
from vendr_web import VendrWebScraper

product_queue = queue.Queue()
result_queue = queue.Queue()


def worker_scraper():
    scrapper = VendrWebScraper()
    while True:
        try:
            scrapped_url = product_queue.get(timeout=3)
            if scrapped_url == "STOP":  # сигнал завершення
                product_queue.task_done()
                break
        except queue.Empty:
            break

        try:
            print(f"Remaining in queue: {product_queue.qsize() - Config.MAX_WORKER_THREADS}")
            data = scrapper.get_product_data(scrapped_url)
            if data:
                result_queue.put(data)
        except:
            pass


def worker_saver():
    db = Database()
    while True:
        try:
            result = result_queue.get(timeout=2)
            if result == "STOP":  # сигнал завершення
                result_queue.task_done()
                break
            db.insert_product(result)
            result_queue.task_done()
        except:
            time.sleep(1)
