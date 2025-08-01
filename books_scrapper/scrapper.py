import re
import time
from typing import Dict, List
from urllib.parse import urljoin

from playwright.sync_api import sync_playwright

from config import Config


class BookScraper:
    def __init__(self):
        self.headless = True
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        self.page = self.browser.new_page()
        self.timer = Config.TIMER

    def close(self):
        self.page.close()
        self.browser.close()
        self.playwright.stop()

    def get_book_data(self, url: str) -> Dict:
        """
        Scraps full data from the book

        :param url: url of the book
        :return: scraped book data
        """
        self.page.goto(url)

        # Title
        title = self.page.locator(".product_main h1").inner_text()

        # Category
        category = self.page.locator("ul.breadcrumb li:nth-child(3) a").inner_text()

        # Price
        price = self.page.locator(".product_main .price_color").inner_text().replace('£', '')
        price = float(price)

        # Rating (via class name)
        rating_class = self.page.locator(".product_main .star-rating").get_attribute("class")
        rating = rating_class.split()[-1]  # Use stars to get rating

        # Stock availability
        stock_text = self.page.locator(".availability").first.inner_text()
        stock = re.search(r"\d+", stock_text)
        stock_availability = stock.group() if stock else "0"

        # Image URL
        img_rel_url = self.page.locator(".thumbnail img").get_attribute("src")
        image_url = f"https://books.toscrape.com/{img_rel_url.lstrip('../')}"

        # Description
        description_locator = self.page.locator("#product_description + p")
        description = description_locator.inner_text() if description_locator.count() > 0 else ""

        # Product Info Table
        info_rows = self.page.locator("table.table.table-striped tr")
        product_info = {}
        for i in range(info_rows.count()):
            key = info_rows.nth(i).locator("th").inner_text()
            value = info_rows.nth(i).locator("td").inner_text()
            product_info[key] = value

        return {
            "title": title,
            "category": category,
            "price": price,
            "rating": rating,
            "stock_availability": stock_availability,
            "image_url": image_url,
            "description": description,
            "product_info": product_info
        }

    def get_all_book_urls(self, start_url: str) -> List[str]:
        """
        Get all book urls from a given url

        :param start_url: url to start from
        """
        urls = []
        next_page = start_url

        while next_page:
            time.sleep(self.timer)
            self.page.goto(next_page)

            links = self.page.locator(".product_pod h3 a")
            for i in range(links.count()):
                href = links.nth(i).get_attribute("href")
                abs_url = urljoin(next_page, href)
                urls.append(abs_url)

            if self.page.locator("ul.pager li.next a").count() > 0:
                rel_next = self.page.locator("ul.pager li.next a").get_attribute("href")
                next_page = urljoin(next_page, rel_next)
            else:
                next_page = None

        self.close()
        return urls
