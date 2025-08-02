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

    def get_category_data(self, category: str) -> str | None:
        """
        Get category data

        :param category: endpoint to get data from
        :param params: parameters to pass to request
        """
        url = f"{self.BASE_URL}{category}"
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
            while True:
                clean_url = subcategory.split("?page=")[0]
                data_page = f"{clean_url}?page={page}"
                page_products_data = self.get_category_data(data_page)

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
