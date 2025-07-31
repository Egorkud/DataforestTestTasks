import logging
from typing import Any, Optional, Union, Dict

import requests

from config import Config

logger = logging.getLogger(__name__)


class VendrAPIClient:
    BASE_URL = "https://api.vendr.com/v1"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "User-Agent": Config.USER_AGENT,
        }

    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Union[Dict[str, Any], list]]:
        """
        Protected GET data from api endpoint

        :param endpoint: endpoint to get data from
        :param params: parameters to pass to request
        """
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as ex:
            logger.exception("Unexpected error during GET request", exc_info=ex)

    def get_categories(self, limit=1000, offset=0, parent_id=None) -> Optional[Union[Dict[str, Any], list]]:
        """
        Method to get category data

        :param limit: maximum number of categories to return
        :param offset: offset of data to return
        :param parent_id: id of parent category
        :return: list of categories or None
        """
        params: Dict[str, Any] = {
            "limit": limit,
            "offset": offset,
            "sortBy": "name",
            "sortOrder": "asc",
        }
        if parent_id:
            params["parentCategoryId"] = parent_id

        return self._get("/catalog/categories", params=params)
