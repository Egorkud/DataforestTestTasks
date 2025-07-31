from config import Config
from vendr_api import VendrAPIClient

if __name__ == "__main__":
    api_client = VendrAPIClient(api_key=Config.VENDR_API_KEY)
    categories = api_client.get_categories(limit=5)

    if categories:
        for category in categories.get(...):
            print(f"- {category['name']} (ID: {category['id']})")
    else:
        print("Не вдалося отримати категорії")
