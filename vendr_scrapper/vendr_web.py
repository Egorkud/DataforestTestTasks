import logging

import requests
from bs4 import BeautifulSoup
from requests import Response

from config import Config

logger = logging.getLogger(__name__)


class VendrWebScraper:
    BASE_URL = "https://www.vendr.com/categories/"

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
        categories = []
        for category in soup_categories:
            categories.append(category.find("a").get("href"))

        return categories
