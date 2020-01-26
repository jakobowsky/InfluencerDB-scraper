# from scrap import InstagramScraper
import requests


class DiscoverBot:
    def __init__(self):
        self.base_url = 'http://127.0.0.1:8000/api/'

    def start_bot(self):
        pass

    def discover_new_accounts_through_hashtags(self, hashtags, category):
        pass

    def get_categories(self):
        link_to_categories = f"{self.base_url}categories"
        categories = requests.get(link_to_categories).json()
        if categories:
            for category in categories:
                print(category)
                hashtags = self.get_hashtags_from_category(category.get("id"))


    def get_hashtags_from_category(self, category_id):
        link_to_hashtags = f"{self.base_url}hashtags?category__id={category_id}"
        hashtags = requests.get(link_to_hashtags).json()
        return [hashtag['name'] for hashtag in hashtags]

DiscoverBot().get_categories()
