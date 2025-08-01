import re
from typing import Dict

from playwright.sync_api import sync_playwright


class BookScraper:
    def __init__(self, headless: bool = True):
        self.headless = headless

    def get_book_data(self, url: str) -> Dict:
        """
        Scraps full data from the book

        :param url: url of the book
        :return: scraped book data
        """
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            page = browser.new_page()
            page.goto(url)

            # Title
            title = page.locator(".product_main h1").inner_text()

            # Category
            category = page.locator("ul.breadcrumb li:nth-child(3) a").inner_text()

            # Price
            price = page.locator(".product_main .price_color").inner_text().replace('£', '')
            price = float(price)

            # Rating (via class name)
            rating_class = page.locator(".product_main .star-rating").get_attribute("class")
            rating = rating_class.split()[-1]  # Use stars to get rating

            # Stock availability
            stock_text = page.locator(".availability").inner_text()
            stock = re.search(r"\d+", stock_text)
            stock_availability = stock.group() if stock else "0"

            # Image URL
            img_rel_url = page.locator(".thumbnail img").get_attribute("src")
            image_url = f"https://books.toscrape.com/{img_rel_url.lstrip('../')}"

            # Description
            description_locator = page.locator("#product_description + p")
            description = description_locator.inner_text() if description_locator.count() > 0 else ""

            # Product Info Table
            info_rows = page.locator("table.table.table-striped tr")
            product_info = {}
            for i in range(info_rows.count()):
                key = info_rows.nth(i).locator("th").inner_text()
                value = info_rows.nth(i).locator("td").inner_text()
                product_info[key] = value

            browser.close()

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
