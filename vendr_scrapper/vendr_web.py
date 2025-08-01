import logging
from typing import Any, Optional, Dict

import requests
from requests import Response

from config import Config

logger = logging.getLogger(__name__)


class VendrWebScraper:
    BASE_URL = "https://www.vendr.com/categories/"

    def __init__(self):
        self.headers = {
            "User-Agent": Config.USER_AGENT,
        }

    def get_category_data(self, category: str, params: Optional[Dict[str, Any]] = None) -> Response | None:
        """
        Protected GET data from api endpoint

        :param category: endpoint to get data from
        :param params: parameters to pass to request
        """
        url = f"{self.BASE_URL}{category}"
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.content
        except Exception as ex:
            logger.exception("Unexpected error during GET request", exc_info=ex)
