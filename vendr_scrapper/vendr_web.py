import logging

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from config import Config

logger = logging.getLogger(__name__)


class VendrWebScraper:
    BASE_URL = "https://www.vendr.com"

    def __init__(self):
        self.headers = {
            "User-Agent": Config.USER_AGENT,
        }

    def get_data_from_url(self, url: str) -> str | None:
        """
        Get category data

        :param url: url to get data from
        """
        url = f"{self.BASE_URL}{url}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except Exception as ex:
            logger.exception("Unexpected error during GET request", exc_info=ex)

    @staticmethod
    def get_subcategories_urls(category_data: str) -> list[str]:
        """
        Get subcategories urls: "/categories/devops/application-development?page=1"

        :param category_data: Category data from vendr.com
        :return: List of subcategories urls
        """
        soup = BeautifulSoup(category_data, "lxml")
        soup_categories = soup.find_all("div", class_="rt-Box rt-r-pb-1")
        subcategories = []
        for category in soup_categories:
            subcategories.append(category.find("a").get("href"))

        return subcategories

    def get_subcategory_product_urls(self, subcategories_urls: list[str]) -> list[str]:
        """
        Collect subcategory product urls from subcategory urls. Goes through each page

        :param subcategories_urls: URLs to get subcategory products
        :return: List of subcategory product urls
        """
        urls = []
        for subcategory in tqdm(subcategories_urls, desc="Getting subcategory product urls"):
            page = 1
            while page < 2:  # 2 For faster testing (True)
                clean_url = subcategory.split("?page=")[0]
                data_page = f"{clean_url}?page={page}"
                page_products_data = self.get_data_from_url(data_page)

                soup_page = BeautifulSoup(page_products_data, "lxml")
                try:
                    products_data = (soup_page.find("div",
                                                    class_="rt-Grid rt-r-gtc-1 sm:rt-r-gtc-2 rt-r-ai-start rt-r-gap-5")
                                     .find_all("a"))
                    for product in products_data:
                        urls.append(product.get("href"))
                except:
                    break
                page += 1
        return urls

    def get_product_data(self, product_urls: list[str]):

        def clean_price_number(price: str) -> str:
            """
            Clean price number from different symbols

            :param price: Price number
            :return: Cleaned price number
            """
            if "$" in price:
                price = price.replace("$", "")

            if "," in price:
                price = price.replace(",", "")

            return price

        for product_url in tqdm(product_urls, desc="Getting product urls"):
            product_page = self.get_data_from_url(product_url)
            soup = BeautifulSoup(product_page, "lxml")

            # Product name
            product_name = (soup.find("div", class_="rt-Flex rt-r-fd-column rt-r-w sm:rt-r-w")
                            .find("div", class_="rt-Flex rt-r-gap-2")
                            .find("h1").text)

            # High - Low prices
            prices_block = (soup.find("div", class_="rt-Grid rt-r-gtc rt-r-ai-center rt-r-mt _rangeSlider_118fo_13")
                            .find_all("span"))
            high_price, low_price = clean_price_number(prices_block[1].text), clean_price_number(prices_block[0].text)

            # Median price
            median_price = clean_price_number(soup.find("div", class_="rt-Flex _rangeAverage_118fo_42").text.split()[1])

            # Description
            description = soup.find("div", class_="rt-Box _read-more-box__content_122o3_1").text


            # TODO: add category + subcatogory to data
            # TODO: add save to DB
