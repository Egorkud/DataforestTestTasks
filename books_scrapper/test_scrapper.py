import multiprocessing
from contextlib import contextmanager
from typing import Any

from tqdm import tqdm

from config import Config
from scrapper import BookScraper


def scrape_worker(book_urls: list[str]) -> list[Any] | None:
    worker = BookScraper()
    full_data = []
    try:
        for url in tqdm(book_urls, desc="Worker scraping:"):
            try:
                data = worker.get_book_data(url)
                full_data.append(data)
            except Exception as e:
                print(f"Failed to scrape {url}: {e}")
        return full_data
    except Exception as e:
        print(f"Failed to scrape: {e}")


if __name__ == "__main__":
    @contextmanager
    def book_scraper_context():
        worker = BookScraper()
        try:
            yield worker
        finally:
            worker.close()


    with book_scraper_context() as scraper:
        urls = scraper.get_all_book_urls("https://books.toscrape.com/")

        print(f"Total books to scrape: {len(urls)}")

        # Кількість потоків
        num_workers = Config.MAX_WORKER_THREADS

        # Розбиваємо список на рівні частини
        chunk_size = (len(urls) + num_workers - 1) // num_workers
        url_chunks = [urls[i:i + chunk_size] for i in range(0, len(urls), chunk_size)]

        # TODO: add to DB
        # Запуск обробки даних кожної книжки
        with multiprocessing.Pool(processes=num_workers) as pool:
            results_nested = pool.map(scrape_worker, url_chunks)

        # Об'єднуємо списки результатів з кожного воркера
        results = [item for sublist in results_nested for item in sublist]
        print("All data saved")
