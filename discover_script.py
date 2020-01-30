from scrap import InstagramScraper
import requests
import time
import random
from typing import Dict, List


class DiscoverBot:
    def __init__(self):
        self.base_url = 'http://127.0.0.1:8000/api/'
        self.scraper = InstagramScraper()
        self.headers = {'Content-type': 'application/json', 'Accept': '*/*'}

    def start_bot(self):
        categories = self.get_categories()
        if categories:
            for category in categories:  # category is a dict
                number_of_hashtags = random.randint(1, 6)
                print(f"Number of hashtags random = {number_of_hashtags}")
                print("Looking for hashtags...")
                hashtags = self.get_hashtags_from_category(category.get("id"))
                if hashtags:
                    hashtags = hashtags[:number_of_hashtags]
                else:
                    print("no hashtags to this category...")
                    continue
                self.discover_new_accounts_through_hashtags(hashtags, category)
                print("Sleeping for next category...")
                time.sleep(random.randint(30, 100))
        print("Finished.")

    def check_if_account_exists(self, username):
        print(f"Checking if {username} is in db.")
        link = f"{self.base_url}instagram_accounts?username={username}"
        response = requests.get(link).json()
        if response:
            print("Account exists.")
            return True
        return False

    def add_account_to_db(self, account: str, category: Dict):
        print(f"Adding {account} to db")
        link_to_adding_account = f'{self.base_url}add_new_account/'
        profile_page_metrics, profile_page_recent_posts = self.scraper.get_current_profile_info(account)
        body = {
            'account': account,
            'category': category,
            'profile_page_metrics': profile_page_metrics,
            'profile_page_recent_posts': profile_page_recent_posts,
        }
        r = requests.post(link_to_adding_account, json=body, headers=self.headers)
        if r.status_code == 200:
            return True
        else:
            return False

    def update_db_with_users(self, accounts: List[str], category: Dict):
        for account in accounts:
            if not self.check_if_account_exists(account):
                if self.add_account_to_db(account, category):
                    print("Added account to db.")
                else:
                    print(f"Something went wrong while adding {account} account to db.")

    def discover_new_accounts_through_hashtags(self, hashtags: List[str], category: Dict):
        for hashtag in hashtags:
            accounts = self.scraper.discover_accounts_from_hashtag(hashtag)
            self.update_db_with_users(accounts, category)
            time.sleep(3)

    def get_categories(self):
        # {'id': 4, 'name': 'Technology'} <-- example of category
        link_to_categories = f"{self.base_url}categories"
        categories = requests.get(link_to_categories).json()
        return categories

    def get_hashtags_from_category(self, category_id):
        link_to_hashtags = f"{self.base_url}hashtags?category__id={category_id}"
        hashtags = requests.get(link_to_hashtags).json()
        return [hashtag['name'] for hashtag in hashtags]


if __name__ == '__main__':
    bot = DiscoverBot()
    bot.start_bot()
