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
        for hashtag in self.basic_hashtags:


    def add_new_hashtags_to_db(self, hashtags):
        # here just post request with all_hashtags, handle on backend site
        pass

    def __add_category(self):
        link_to_category = f'{self.base_url}categories'
        body = {
            "name": f"{self.category.title()}"
        }
        r = requests.post(link_to_category,data=body)
        if r.status_code == 200:
            print("Added new category to db: ", r.json())
            return True
        else:
            print("Smth went wrong: ", r.json())
            raise

    def add_category_to_db(self):
        link_to_category = f'{self.base_url}categories?name={self.category}'
        try:
            response = requests.get(link_to_category).json()
            if response[0].get('name').title() == self.category:
                print("This category is already in db.")
                amount_of_hashtags = self.check_amount_current_hashtags()
                print(f'It has {amount_of_hashtags} hashtags.')
                if amount_of_hashtags < 4:
                    pass
                    # explore new hashtags
            else:
                print("This category is not in db. Adding and finding hashtags.")
                if self.__add_category():
                    pass
                    # explore new hashtags
                # if success then find hashtags and add them

        except Exception as e:
            print("ERROR: ", e)


x = HashtagScript('technology', '')
x.add_category_to_db()
