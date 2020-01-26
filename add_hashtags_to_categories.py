from scrap import InstagramScraper
import requests


class HashtagScript:

    def __init__(self, category, basic_hashtags):
        self.scraper = InstagramScraper()
        self.base_url = 'http://127.0.0.1:8000/api/'
        self.category = category.title()
        self.basic_hashtags = basic_hashtags

    def __call__(self, *args, **kwargs):
        pass

    def check_current_hashtags(self):
        links_to_hashtags = f'{self.base_url}hashtags?category__name={self.category}'
        try:
            response = requests.get(links_to_hashtags).json()
            return response
        except Exception as e:
            print("ERROR: ", e)

    def check_amount_current_hashtags(self):
        return len(self.check_current_hashtags())

    def find_new_hashtags(self):
        pass

    def add_new_hashtags_to_db(self, hashtags):
        # here just post request with all_hashtags, handle on backend site
        pass

    def add_category_to_db(self):
        link_to_category = f'{self.base_url}categories?name={self.category}'
        try:
            response = requests.get(link_to_category).json()
            if response[0].get('name').title() == self.category:
                print("This category is already in db.")
                amount_of_hashtags = self.check_amount_current_hashtags()
                print(f'It has {amount_of_hashtags} hashtags.')

            print(response)
        except Exception as e:
            print("ERROR: ", e)


x = HashtagScript('technology', '')
x.add_category_to_db()
